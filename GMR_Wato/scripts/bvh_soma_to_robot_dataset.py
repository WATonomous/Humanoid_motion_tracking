"""Retarget a whole folder of SOMA BVHs (BONES-SEED) with GMR, in parallel, to GMR pkl files.

Put it in GMR_Wato/scripts/ and run from GMR_Wato/:

    python scripts/bvh_soma_to_robot_dataset.py \
        --src_folder ~/data/bones-seed/soma_uniform/bvh \
        --tgt_folder ~/data/bones-seed/pioneer_gmr \
        --robot pioneer_humanoid --target_fps 30 --workers 8 --no_mirror

    # only the clips in a list, e.g. MimicLite's limmt/passed/filenames.txt (lines like 210531/<motion>.npz)
    ... --list sonic_views/limmt/passed/filenames.txt

The folder tree is kept (<tgt>/<date>/<motion>.pkl). Clips already done are skipped, so an interrupted run
resumes where it stopped. Failures go to <tgt>/failed.txt. The pkl is the same as bvh_to_robot.py --save_path
writes (fps, root_pos, root_rot xyzw, dof_pos), so batch_gmr_pkl_to_csv.py works on it.
"""
import argparse
import os
import pickle
import time
import traceback
from multiprocessing import Pool

import numpy as np

SRC_FPS = 120  # BONES-SEED
_RT = {}  # one retargeter per worker process: building it loads the robot's meshes (~9 s for pioneer)


def retarget_one(job):
    bvh, out, robot, step, fps = job
    from general_motion_retargeting import GeneralMotionRetargeting as GMR
    from general_motion_retargeting.utils.lafan1 import load_bvh_file

    try:
        frames, height = load_bvh_file(bvh, format="soma")
        frames = frames[::step]
        if (robot, height) not in _RT:
            _RT[(robot, height)] = GMR(src_human="bvh_soma", tgt_robot=robot, actual_human_height=height, verbose=False)
        rt = _RT[(robot, height)]
        # start at the first frame's root from the default pose, as bvh_to_robot.py does
        rt.update_targets(frames[0])
        root = rt.human_body_to_task2[rt.human_root_name].transform_target_to_world
        q = rt.model.qpos0.copy()
        q[3:7], q[:3] = root.wxyz_xyz[:4], root.wxyz_xyz[4:]
        rt.configuration.update(q)
        qpos = np.array([rt.retarget(f).copy() for f in frames])
        motion = {
            "fps": fps,
            "root_pos": qpos[:, :3],
            "root_rot": qpos[:, [4, 5, 6, 3]],  # wxyz -> xyzw
            "dof_pos": qpos[:, 7:],
            "local_body_pos": None,
            "link_body_list": None,
        }
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out + ".part", "wb") as f:
            pickle.dump(motion, f)
        os.replace(out + ".part", out)
        return bvh, None
    except Exception:
        return bvh, traceback.format_exc(limit=3)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src_folder", required=True)
    ap.add_argument("--tgt_folder", required=True)
    ap.add_argument("--robot", default="pioneer_humanoid")
    ap.add_argument("--target_fps", type=int, default=30, help="120 must be divisible by it")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--no_mirror", action="store_true", help="skip the mirrored copies (*_M.bvh)")
    ap.add_argument("--only", nargs="*", help="only files whose path contains one of these")
    ap.add_argument("--list", help="text file of <date>/<motion>[.ext] lines: retarget only those")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--override", action="store_true")
    args = ap.parse_args()

    src, tgt = os.path.abspath(os.path.expanduser(args.src_folder)), os.path.abspath(os.path.expanduser(args.tgt_folder))
    step = SRC_FPS // args.target_fps
    wanted = None
    if args.list:
        wanted = {os.path.splitext(l.strip())[0] for l in open(os.path.expanduser(args.list)) if l.strip()}
    jobs = []
    for dirpath, _, names in os.walk(src):
        for n in sorted(names):
            if not n.endswith(".bvh") or (args.no_mirror and n.endswith("_M.bvh")):
                continue
            bvh = os.path.join(dirpath, n)
            if args.only and not any(s in bvh for s in args.only):
                continue
            if wanted is not None and f"{os.path.basename(dirpath)}/{n[:-4]}" not in wanted:
                continue
            out = os.path.join(tgt, os.path.relpath(bvh, src))[:-4] + ".pkl"
            if os.path.exists(out) and not args.override:
                continue
            jobs.append((bvh, out, args.robot, step, args.target_fps))
    jobs = jobs[: args.limit]
    print(f"{len(jobs)} clips to retarget with {args.workers} workers")

    os.makedirs(tgt, exist_ok=True)
    t0, done, failed = time.time(), 0, 0
    with Pool(args.workers) as pool, open(os.path.join(tgt, "failed.txt"), "a") as log:
        for bvh, err in pool.imap_unordered(retarget_one, jobs):
            done += 1
            if err:
                failed += 1
                log.write(f"{bvh}\n{err}\n")
                log.flush()
            if done % 50 == 0 or done == len(jobs):
                rate = done / (time.time() - t0)
                print(f"{done}/{len(jobs)}  failed {failed}  {rate:.2f} clips/s  "
                      f"~{(len(jobs) - done) / rate / 3600:.1f} h left", flush=True)
    print("done:", tgt)
