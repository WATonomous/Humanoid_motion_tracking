# Wato Whole Body Motion Tracking Pipeline

Whole Body Motion tracking pipeline adapted for the **WATonomous (Wato) humanoid robot**:

- **[GMR](https://github.com/YanjieZe/GMR)** (General Motion Retargeting): retargets human motion onto robot motion.
- **[BeyondMimic `whole_body_tracking`](https://github.com/HybridRobotics/whole_body_tracking)**: physics-aware reinforcement learning, configured for **Isaac Sim 5.1 + Isaac Lab 2.3**, with:
  - a custom CSV → NPZ converter for the Wato robot (`scripts/csv_to_npz_wato.py`)
  - a custom Wato robot config (`robots/wato.py`)
  - Wato task registration for training (`Tracking-Flat-Wato-v0`)

```
Human motion (BVH) ──GMR──▶ robot motion (PKL) ──▶ CSV ──▶ NPZ ──▶ BeyondMimic training ──▶ evaluation
```

## Repository layout

```
.
├── convert_motion.sh        # whole pipeline: BVH -> PKL -> CSV -> NPZ
├── GMR_Wato/                # GMR with the watonomous robot
└── whole_body_tracking/     # BeyondMimic with the Wato robot config and tasks
```

## Installation

### GMR
Go into the GMR folder and follow its installation guide:

```bash
cd GMR_Wato
# follow the installation instructions in GMR_Wato/README.md
```

### whole_body_tracking
Use **Isaac Sim 5.1 + Isaac Lab 2.3**, then follow the instructions in `whole_body_tracking` as is:

```bash
cd whole_body_tracking
# follow the installation instructions in whole_body_tracking/README.md
```

## Usage

### Full pipeline: `convert_motion.sh`

For ease of use, `convert_motion.sh` runs the whole pipeline from **BVH → NPZ** for BeyondMimic training. The final NPZ is uploaded to the WandB motion registry.

```bash
./convert_motion.sh --file_path path/to/motion.bvh
```

| Option | Description |
|---|---|
| `--file_path` | **Required.** Path to the input BVH file |
| `--input_fps` | Frame rate of the BVH. Optional: read from the BVH's `Frame Time` if omitted |
| `--name` | Name of the motion (output files and WandB registry entry). Defaults to the BVH file name |
| `--robot` | GMR robot name. Defaults to `watonomous` |

**Different conda environment names:** the script uses `gmr` for GMR and `isaaclab_test` for Isaac Lab. If yours are named differently, set them when running the script:

```bash
GMR_ENV=my_gmr_env ISAAC_ENV=my_isaaclab_env ./convert_motion.sh --file_path path/to/motion.bvh
```

### Step by step

GMR accepts several types of input motion; **currently only Xsens has been tested**.

#### 1. Xsens BVH → PKL (GMR retargeting)

Make sure the Xsens BVH is exported in **3DSM** format.

```bash
python scripts/xsens_bvh_to_robot.py \
    --bvh_file "$FILE_PATH" \
    --robot watonomous \
    --save_path "$PKL_FILE" \
    --scale 0.01 \
    --reset_to_zero \
    --bvh_format 3DSM
```

Outputs a PKL file retargeted for the Wato robot.

#### 2. PKL → CSV

```bash
python "${GMR_DIR}/convert_gmr_xsens.py" --target_file "$PKL_FILE" --output_file "$CSV_FILE"
```

A custom script that converts the PKL to the CSV format BeyondMimic expects, and also fixes the quaternion ordering.

#### 3. CSV → NPZ (Wato robot)

Run from the `whole_body_tracking` folder. Replays the CSV on the Wato robot in Isaac Sim 5.1 / Isaac Lab 2.3, resamples it to 50 fps (the rate BeyondMimic trains at) and uploads the NPZ to the WandB motion registry. `--input_fps` must be the frame rate of the original recording.

```bash
python scripts/csv_to_npz_wato.py \
    --input_file whole_body_humanoid/wato_boxing.csv \
    --input_fps 120 \
    --output_name wato_boxing \
    --output_fps 50
```

### Training

Trains a tracking policy on the Wato robot with the registered `Tracking-Flat-Wato-v0` task, using a motion from the WandB registry:

```bash
python scripts/rsl_rl/train.py \
    --task=Tracking-Flat-Wato-v0 \
    --registry_name=szlgm2018-university-of-waterloo-org/wandb-registry-motions/wato_boxing \
    --num_envs 4096 \
    --max_iterations 30000 \
    --headless \
    --logger wandb \
    --log_project_name wato_tracking \
    --run_name boxing_v1
```

### Evaluation

Plays a trained policy through the whole motion, from start to finish:

```bash
python scripts/rsl_rl/play_full_motion.py \
    --task=Tracking-Flat-Wato-v0 \
    --wandb_path=szlgm2018-university-of-waterloo/wato_tracking/j1ziddpb \
    --num_envs 1 \
    --video
```

This saves a **real-time** MP4 video of the robot following the policy.

> **Note:** the default `play.py` and `replay_npz.py` viewers are **not** real time by default: their playback speed depends on how fast your PC can step the simulation. Use the `--video` output to judge the true speed of a motion.
