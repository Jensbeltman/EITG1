import rtde_receive
import rtde_control
import click
import numpy as np
import uuid
import matplotlib.pyplot as plt
import time

robot_ip = "192.168.100.2"
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
rtde_c = rtde_control.RTDEControlInterface(robot_ip)

def plot_value_hist(pose_hist, name_mode=None):
    plt.figure()
    els = np.array(pose_hist).T

    for i, el in enumerate(els):
        name = f"{i}"
        if name_mode is not None:
            name = plot_value_hist.names[name_mode][i]

        plt.plot(el, label=name)

    plt.grid()
    plt.legend()
    plt.show()
plot_value_hist.names={
    "pose": ["x", "y", "z", "r1", "r2", "r3"],
    "force": ["Fx", "Fy", "Fz", "Fr1", "Fr2", "Fr3"]
}

def force_drive(start_height, end_height, speed=0.25, force_down=10, pro_stop=0.95, sleep=0.5):
    pose_hist = []
    force_hist = []

    start_pose = rtde_r.getActualTCPPose()
    start_pose[2] = start_height
    rtde_c.moveP(start_pose, speed, 2, 0.0)

    task_frame = start_pose
    selection_vector = [0, 0, 1, 0, 0, 0]
    wrench_up = [0, 0, force_down, 0, 0, 0]
    force_type = 2
    limits = [2] * 6  # [1, 1, 1, 1, 1, 1]

    go_on_at = pro_stop * force_down  # 80%

    time.sleep(sleep)

    # Execute 500Hz control loop for 4 seconds, each cycle is 2ms
    while True:
        # First move the robot down for 2 seconds, then up for 2 seconds

        rtde_c.forceMode(task_frame, selection_vector, wrench_up, force_type, limits)

        act_pose = rtde_r.getActualTCPPose()
        pose_hist.append(act_pose)
        force = rtde_r.getActualTCPForce()
        force_hist.append(force)

        if force[2] >= go_on_at:
            break

    rtde_c.forceModeStop()

    start_pose[2] = end_height
    rtde_c.moveP(start_pose, speed, 2, 0.0)

    return pose_hist, force_hist


def force_test(force, start_h=0.15, end_h=0.25, speed_to_h=0.25, pro_stop=0.95):
    awn = click.prompt(f"Start first force test? ({force} N)", type=str, default="y")
    awn = awn.lower()

    if awn == "y":
        pose_hist, force_hist = force_drive(start_h, end_h, speed=speed_to_h, force_down=force, pro_stop=pro_stop)
    else:
        return

    run_id = str(uuid.uuid4())
    np.save(f"force_test_{force}_poseHist_{run_id}.npy", pose_hist)
    np.save(f"force_test_{force}_forceHist_{run_id}.npy", force_hist)

    damage_awn = click.prompt(f"Is there any damage?", type=str, default="yes")
    with open(f"force_test_{force}_damage_{run_id}.txt", "w") as f:
        f.write(damage_awn)

    plot_value_hist(pose_hist, name_mode="pose")
    plot_value_hist(force_hist, name_mode="force")


for force in np.linspace(1, 30, 15, dtype=int):
    force_test(force, start_h=0.15, end_h=0.15, speed_to_h=0.15, pro_stop=0.95)

print("Done!!!!!!")
