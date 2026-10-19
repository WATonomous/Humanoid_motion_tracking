# Joint proof (MuJoCo forward kinematics)

67 joints, 68 bodies. Each joint alone at 60 % of its range; its child link must turn by that angle and its parent must stay still.

| joint | range (deg) | tested (deg) | child link | child turned (deg) | farthest link moved (mm) | links driven | result |
|---|---|---|---|---|---|---|---|
| waist_yaw | -90 .. 90 | 54 | torso | 54.0 | 268 | 55 | PASS |
| r_shoulder_pitch | -180 .. 180 | 108 | r_arm_link1 | 108.0 | 1400 | 27 | PASS |
| r_shoulder_roll | -90 .. 90 | 54 | r_arm_link2 | 54.0 | 786 | 26 | PASS |
| r_upper_arm_yaw | -90 .. 90 | 54 | r_arm_link3 | 54.0 | 85 | 25 | PASS |
| r_elbow | -90 .. 90 | 54 | r_arm_link4 | 54.0 | 512 | 24 | PASS |
| r_forearm_roll | -90 .. 90 | 54 | r_forearm | 54.0 | 86 | 23 | PASS |
| r_wrist_dev | -20 .. 30 | 18 | r_hand_W | 18.0 | 73 | 22 | PASS |
| r_wrist_flex | -60 .. 60 | 36 | r_hand_H | 36.0 | 130 | 21 | PASS |
| r_abd | -15 .. 15 | 9 | r_hand_U | 9.0 | 12 | 4 | PASS |
| r_mcp | 0 .. 90 | 54 | r_hand_P | 54.0 | 63 | 3 | PASS |
| r_pip | 0 .. 90 | 54 | r_hand_I | 54.0 | 30 | 2 | PASS |
| r_dip | 0 .. 90 | 54 | r_hand_D | 54.0 | 0 | 1 | PASS |
| r_i_abd | -15 .. 15 | 9 | r_hand_U_I | 9.0 | 12 | 4 | PASS |
| r_i_mcp | 0 .. 90 | 54 | r_hand_P_I | 54.0 | 63 | 3 | PASS |
| r_i_pip | 0 .. 90 | 54 | r_hand_I_I | 54.0 | 30 | 2 | PASS |
| r_i_dip | 0 .. 90 | 54 | r_hand_D_I | 54.0 | 0 | 1 | PASS |
| r_r_abd | -15 .. 15 | 9 | r_hand_U_R | 9.0 | 12 | 4 | PASS |
| r_r_mcp | 0 .. 90 | 54 | r_hand_P_R | 54.0 | 63 | 3 | PASS |
| r_r_pip | 0 .. 90 | 54 | r_hand_I_R | 54.0 | 30 | 2 | PASS |
| r_r_dip | 0 .. 90 | 54 | r_hand_D_R | 54.0 | 0 | 1 | PASS |
| r_l_abd | -15 .. 15 | 9 | r_hand_U_L | 9.0 | 12 | 4 | PASS |
| r_l_mcp | 0 .. 90 | 54 | r_hand_P_L | 54.0 | 63 | 3 | PASS |
| r_l_pip | 0 .. 90 | 54 | r_hand_I_L | 54.0 | 30 | 2 | PASS |
| r_l_dip | 0 .. 90 | 54 | r_hand_D_L | 54.0 | 0 | 1 | PASS |
| r_th_c | 0 .. 50 | 30 | r_hand_TC | 30.0 | 44 | 4 | PASS |
| r_th_f | 0 .. 60 | 36 | r_hand_TF | 36.0 | 40 | 3 | PASS |
| r_th_mcp | 0 .. 80 | 48 | r_hand_TP | 48.0 | 33 | 2 | PASS |
| r_th_ip | 0 .. 80 | 48 | r_hand_TD | 48.0 | 0 | 1 | PASS |
| l_shoulder_pitch | -180 .. 180 | 108 | l_arm_link1 | 108.0 | 1400 | 27 | PASS |
| l_shoulder_roll | -90 .. 90 | 54 | l_arm_link2 | 54.0 | 786 | 26 | PASS |
| l_upper_arm_yaw | -90 .. 90 | 54 | l_arm_link3 | 54.0 | 85 | 25 | PASS |
| l_elbow | -90 .. 90 | 54 | l_arm_link4 | 54.0 | 512 | 24 | PASS |
| l_forearm_roll | -90 .. 90 | 54 | l_forearm | 54.0 | 86 | 23 | PASS |
| l_wrist_dev | -20 .. 30 | 18 | l_hand_W | 18.0 | 73 | 22 | PASS |
| l_wrist_flex | -60 .. 60 | 36 | l_hand_H | 36.0 | 130 | 21 | PASS |
| l_abd | -15 .. 15 | 9 | l_hand_U | 9.0 | 12 | 4 | PASS |
| l_mcp | 0 .. 90 | 54 | l_hand_P | 54.0 | 63 | 3 | PASS |
| l_pip | 0 .. 90 | 54 | l_hand_I | 54.0 | 30 | 2 | PASS |
| l_dip | 0 .. 90 | 54 | l_hand_D | 54.0 | 0 | 1 | PASS |
| l_i_abd | -15 .. 15 | 9 | l_hand_U_I | 9.0 | 12 | 4 | PASS |
| l_i_mcp | 0 .. 90 | 54 | l_hand_P_I | 54.0 | 63 | 3 | PASS |
| l_i_pip | 0 .. 90 | 54 | l_hand_I_I | 54.0 | 30 | 2 | PASS |
| l_i_dip | 0 .. 90 | 54 | l_hand_D_I | 54.0 | 0 | 1 | PASS |
| l_r_abd | -15 .. 15 | 9 | l_hand_U_R | 9.0 | 12 | 4 | PASS |
| l_r_mcp | 0 .. 90 | 54 | l_hand_P_R | 54.0 | 63 | 3 | PASS |
| l_r_pip | 0 .. 90 | 54 | l_hand_I_R | 54.0 | 30 | 2 | PASS |
| l_r_dip | 0 .. 90 | 54 | l_hand_D_R | 54.0 | 0 | 1 | PASS |
| l_l_abd | -15 .. 15 | 9 | l_hand_U_L | 9.0 | 12 | 4 | PASS |
| l_l_mcp | 0 .. 90 | 54 | l_hand_P_L | 54.0 | 63 | 3 | PASS |
| l_l_pip | 0 .. 90 | 54 | l_hand_I_L | 54.0 | 30 | 2 | PASS |
| l_l_dip | 0 .. 90 | 54 | l_hand_D_L | 54.0 | 0 | 1 | PASS |
| l_th_c | 0 .. 50 | 30 | l_hand_TC | 30.0 | 44 | 4 | PASS |
| l_th_f | 0 .. 60 | 36 | l_hand_TF | 36.0 | 40 | 3 | PASS |
| l_th_mcp | 0 .. 80 | 48 | l_hand_TP | 48.0 | 33 | 2 | PASS |
| l_th_ip | 0 .. 80 | 48 | l_hand_TD | 48.0 | 0 | 1 | PASS |
| Hip_F_L | -20 .. 90 | 54 | l_hip_pitch_link | 54.0 | 730 | 6 | PASS |
| Hip_A_L | -10 .. 60 | 36 | l_hip_roll_link | 36.0 | 497 | 5 | PASS |
| Hip_R_L | -30 .. 90 | 54 | l_thigh | 54.0 | 6 | 4 | PASS |
| Knee_L | -60 .. 5 | -36 | l_shank_foot | 36.0 | 254 | 3 | PASS |
| Ankle_P_L | -30 .. 50 | 30 | l_ankle_cross | 30.0 | 9 | 2 | PASS |
| Ankle_R_L | -30 .. 30 | 18 | l_foot | 18.0 | 0 | 1 | PASS |
| Hip_F_R | -20 .. 90 | 54 | r_hip_pitch_link | 54.0 | 730 | 6 | PASS |
| Hip_A_R | -10 .. 60 | 36 | r_hip_roll_link | 36.0 | 497 | 5 | PASS |
| Hip_R_R | -30 .. 90 | 54 | r_thigh | 54.0 | 6 | 4 | PASS |
| Knee_R | -60 .. 5 | -36 | r_shank_foot | 36.0 | 254 | 3 | PASS |
| Ankle_P_R | -30 .. 50 | 30 | r_ankle_cross | 30.0 | 9 | 2 | PASS |
| Ankle_R_R | -30 .. 30 | 18 | r_foot | 18.0 | 0 | 1 | PASS |

**67 of 67 pass.**
