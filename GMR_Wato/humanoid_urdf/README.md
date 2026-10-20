# Pioneer humanoid: the URDF of the FINAL design (Oct 18)

The owner's final armV2 humanoid: the graphite SpaceX head (`spacex_traced_head.py`, `SPACEX_DESIGN=graphite`), version
2's torso, the armV2 arms, hands D, the wato legs, with every joint: **67 revolute joints** - a waist yaw, 5 a arm, 22 a
hand (8 DIP joints mimic their PIP), 6 a leg named as the team's model names them (`Hip_F` pitch, `Hip_A` roll, `Hip_R`
yaw, `Knee`, `Ankle_P`, `Ankle_R`, `_L` / `_R`), with its axes and limits. Loads in MuJoCo
(`pioneer_humanoid_mujoco.urdf`, 68 bodies, 67 dof). **Open question**: in the team's model (and so here) a negative
`Knee` swings the shank forward, so its default stance (Knee -0.22) bends the knees backward: a sign to check with them. Likewise a positive `Hip_A` (hip roll, range -10..60 deg) swings the leg inward, across the other leg. Proof of every joint: `joint_proof.md` (67 of 67 move as they should, `joint_proof.py`) and `docs/renders/final_humanoid_joint_sheet.png`. Check render: `docs/renders/archive/humanoid/final_humanoid_urdf_check.png` (zero
pose and a posed one). The earlier URDF (version 1 head, no leg/waist joints beyond the knee and a guessed hip yaw) is
archived in git history.

(What follows is the first URDF's write-up, updated where the final one differs.)

`pioneer_humanoid.urdf` + `meshes/` (153 OBJ with smooth normals, 214 MB, 2.54 M triangles). Written by `make_urdf.py`: change that and re-run it, not the URDF.

    Backend/cad_bench/projects/bimanual_head/setup_scene.sh OUT          # the arm and leg scene, ~3.5 min
    cd Backend && python cad_bench/projects/humanoid_urdf/make_urdf.py OUT     # ~3 min

It needs build123d, trimesh and numpy (no GPU). Checked by loading it with `yourdfpy` and rendering it at the
zero pose and a posed one: `docs/renders/archive/humanoid/humanoid_urdf_check.png`.

`view_urdf.py pioneer_humanoid.urdf out.png ['{"r_elbow": -1.0}'] [--dir x,y,z] [--look x,y,z] [--dist m]` path-traces the
URDF's own meshes in a pose.

**MuJoCo** (3.6) loads `pioneer_humanoid_mujoco.urdf` in 1.0 s: the same file with
`<mujoco><compiler meshdir="meshes" balanceinertia="true" discardvisual="false"/></mujoco>` inside `<robot>`, which
tells it where the meshes are. (MuJoCo refuses an STL of more than 200 000 faces; OBJ has no such limit, and
`make_urdf.py` writes a larger STL in pieces when `URDF_MESH_FORMAT=stl`.)

## What it is

- The robot of the renders: version 1 head, version 2 torso, the armV2 arms down to their forearm motors, the
  tendon forearms and hands ("hands D": ring pack, short motor), the wato legs.
- 59 links, 58 revolute joints (8 of them DIP joints that mimic their PIP), all at zero in the modelled pose.
- Frame: metres, Z up, the robot faces -Y, its right arm at -x, feet on z = -0.02. Every link frame sits at its
  joint's pivot with axes parallel to the base's in the zero pose (so each visual's origin is minus its pivot).
- Colour is written twice: in the URDF's `<material>` and in a `.mtl` beside each OBJ (many viewers draw an OBJ with
  the mesh's own material and ignore the URDF's: without the `.mtl` the robot comes out white there).
- Visuals: one OBJ per link and colour, in the colours the renders use (`COLORS` of each part; bought parts
  without one are the renders' grey). The meshes are in millimetres in the scene's frame and scaled 0.001 in the URDF.
  Re-meshed from the CAD at 1 mm; solids under 12 mm (screws, nuts, pins) are left out. The forearms' insides (the
  20 motors, spools, tendons) are not in it: `HANDS_FULL=1` in the environment adds them (much larger).
- `links.json`: which scene parts make each link, and every joint's pivot (mm) and axis.

## How far to trust each joint

| Joints | Source | Trust |
|---|---|---|
| Hands: `*_wrist_dev`, `*_wrist_flex`, each finger's `abd`, `mcp`, `pip`, `dip`, thumb `th_c`, `th_f`, `th_mcp`, `th_ip` | `finger_drive.py`'s own `AXES`, `CHAIN` and ranges | exact. The left hand is mirrored with its axes reversed, so a positive angle curls both hands the same way. Finger names: no letter = middle, `i` index, `r` ring, `l` little |
| Arms: `shoulder_pitch`, `shoulder_roll`, `upper_arm_yaw`, `elbow`, `forearm_roll` | each joint's motor in the arm STEP: the disc's thin dimension is the axis, its centre the pivot | axes and pivots good to a few mm; **limits are placeholders** |
| Waist: `waist_yaw` | added (Oct 18, the owner): the torso, head, shoulder frame and arms on the pelvis, at z 897 | **no motor in the CAD yet**: the joint the design needs |
| Legs: `Hip_F_*` (pitch), `Hip_A_*` (roll), `Hip_R_*` (yaw), `Knee_*`, `Ankle_P_*`, `Ankle_R_*` | the team's `whole_body_humanoid.urdf` (WATonomous/pioneer_humanoid): its names, chain, world axes and limits (Knee -65..0 deg as Nick's PR #337, Ankle_R +-15 deg: the owner's Oct 20 limits); its spacings land on this CAD's motors to a few mm (the hip pitch motor sits in the pelvis tube, absent from the leg STEP) | as the team's model |

## Not done

- **The knee's sign** (see above): as the team's model has it, to be confirmed.
- **Inertia** is a placeholder (each link's CAD volume at 0.35 g/cm3, as a box). Not for dynamics.
- **Collision** is each link's bounding box.
- **Limits, effort, velocity** on the arms and legs are placeholders (effort 10, velocity 6 everywhere).
- **The neck** is fixed: the head has no neck joint.
- The joint between the arm's forearm motor and the tendon forearm is not designed; here the forearm simply turns
  about that motor's axis from its underside.
- The mesh paths are relative (`meshes/x.obj`): for ROS, wrap this folder in a package and prefix them.

## The showcase videos (`showcase/`, `docs/renders/archive/humanoid/humanoid_*.mp4`)

Five clips, all rendered from the URDF's meshes with no CAD per frame, on the sunlit plaza of
`cad_bench/flight/pbr_flight.py` (2.3 s a frame at 1280 x 720, 48 samples, on an RTX 4060; `--scene studio` is the
white studio, 0.7 s a frame):

| file | shots module | what |
|---|---|---|
| `humanoid_showcase.mp4` | `shots.py` | walk in, wave, a hand up to the visor, the hand's gestures, both hands |
| `humanoid_football.mp4` | `football.py` | a run-up and a kick into a goal |
| `humanoid_weightlifting.mp4` | `weightlifting.py` | a barbell off a rack, two push presses |
| `humanoid_basketball.mp4` | `basketball.py` | a shot through a hoop |
| `humanoid_manipulation.mp4` | `manipulation.py` | a flask picked off a table, passed hand to hand, set down |

    URDF_LEGS=walk URDF_HAND_SKIP_MM=3 URDF_OUT=/tmp/walk_urdf URDF_NAME=pioneer_walk \
        python cad_bench/projects/humanoid_urdf/make_urdf.py OUT
    python cad_bench/projects/humanoid_urdf/showcase/render_anim.py /tmp/walk_urdf/pioneer_walk.urdf \
        cad_bench/projects/humanoid_urdf/showcase/shots.py frames/ --exposure 2.39 [--frames 0,100 --size 640,360 --spp 16]
    ffmpeg -framerate 24 -i frames/f_%05d.png -c:v libx264 -pix_fmt yuv420p -crf 20 out.mp4

- **Animated, not simulated.** Arm poses are solved (palm to a point, facing a direction) and eased between; the
  legs follow a drawn gait; props ride in the hands. Only the balls' flights are ballistic. Nothing checks balance,
  torque, grip or collision, and the basketball goes in because its launch velocity is computed from the rim.
- `URDF_LEGS=walk` writes a copy for animation only: a hip pitch about the pelvis's cross tube (ASSUMED: the CAD has
  hip roll and yaw motors and no pitch drive) and a foot hinged on the ankle's bearings (the ankle motors' push rods
  stay on the shank). It is not the robot's kinematics and is not the URDF kept here.
- The walk (`shots.py`): leg angles from a two-link IK of a foot path, the body moved over the foot that is down.
  Which foot is down comes from the gait's phase, not from which is lower: picking the lower one chose the swinging
  foot for two frames a step and threw the body back 0.2 m (seen as a jolt each step).
- The left arm's joints take the same angles as the right's for the mirrored pose. Two-handed poses solve the right
  arm and copy it (`weightlifting.py`); solved separately the arms reach the same points with different elbows.
- A hand that carries a prop has to reach its target: `manipulation.py` asserts the solver's miss is under 6 mm (a
  5 cm miss once sank the flask into the table). The basketball's low holds miss by more and the grip looks loose.
- Stills did not show what a measurement did: in the flask clip the straight thumb stood 33 mm inside the flask and
  the hands came up through the table top. Now the flask sits where the bent thumb clears it, each finger is curled
  until its skin meets the flask, and a hand rises beside the body before it goes over the table; every link's
  vertices against the flask and the table, frame by frame, are within 3 mm (`showcase/checks.py URDF shots.py`;
  the other clips have not been run through it).
- `make_urdf.py` meshes with the kernel's mesher directly. build123d's `tessellate()` dropped about 2% of the hand
  skins' area as holes. The URDF kept in this folder is regenerated with it.
- **The hand's joints at 0 are a straight hand.** The hands ride the arms in a relaxed pose (`humanoid_hands.POSE`)
  and `finger_drive.py`'s axes are the straight hand's. Written as posed, every joint past a finger's MCP (and the
  thumb past its root) hinged off its pin: the PIP 5 mm out, the DIP in empty space, and a fingertip left its joint
  as it curled (seen in the first renders of these clips, and it would show the same in any simulator).
  `make_urdf.py` now writes each hand link un-posed. Checked by a side-on render of the index finger at 0 to 90 deg
  with markers on the pivots, and by the pinch poses, whose tips now meet (0.5 and 3 mm; 12 and 42 mm before):
  `showcase/checks.py URDF --hand`, also `tests/test_humanoid_urdf.py`.
- Three things the renderer needed to be clean at 48 samples: one environment light instead of several area lights
  (picked at random per sample, they left the robot speckled), a box pixel filter (the denoiser leaves noise that
  a gaussian filter has correlated between pixels), and reloading the scene per frame (moving instances through
  `mi.traverse` was 8 times slower).
