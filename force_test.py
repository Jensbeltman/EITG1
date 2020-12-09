import rtde_receive
import rtde_control
import time
import numpy as np
import matplotlib.pyplot as plt
import math
import uuid

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

def converter(el, from_unit, to_unit):
    """
    Can be done so much better :)
    Parameters
    ----------
    el
    from_unit
    to_unit

    Returns
    -------

    """
    unc = {
        "m": 1,
        "dm": 10,
        "cm": 100,
        "mm": 1000,
    }

    el_in_m = el / unc[from_unit]
    el_out = el_in_m * unc[to_unit]
    return el_out


def limet_check(currentTCP, limetTCP_lower=None, limetTCP_upper=None):
    if limetTCP_lower is not None:
        for el, el_lower in zip(currentTCP, limetTCP_lower):
            if el_lower is not None and el <= el_lower:
                return True
    if limetTCP_upper is not None:
        for el, el_upper in zip(currentTCP, limetTCP_upper):
            if el_upper is not None and el >= el_upper:
                return True
    return False

robot_ip = "192.168.100.2"
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
rtde_c = rtde_control.RTDEControlInterface(robot_ip)

fist_pose = [-0.24126775044997928, -0.42075908202903856, 0.6586334885483427, 2.599420154499895, 0.09288735719897556, -0.6802083104833498]
rtde_c.moveP(fist_pose, 0.6, 2, 0.0)

rock_start_pos = [-0.08203968530815126, -0.5326926026406975, 0.3, -3.0392028741044914, -0.7231190853395795, -0.024991325114571333] #rtde_r.getActualTCPPose()
go_pose = rock_start_pos.copy()
go_to_height = 0.30
go_pose[2] = go_to_height
rtde_c.moveP(go_pose, 0.6, 2, 0.0)


TCP_lower = [None, None, None, None, None, None]
#[None, None, 0.2484923468255163, None, None, None]

pose_hist = []
force_hist = []

speed = converter(1, "cm", "m")
acceleration = 0.5

def force_drive(start_height, end_height, speed=0.25):
    start_pose = rtde_r.getActualTCPPose()
    start_pose[2] = start_height
    rtde_c.moveP(start_pose, speed, 2, 0.0)

    task_frame = start_pose
    force_down = 10
    selection_vector = [0, 0, 1, 0, 0, 0]
    wrench_up = [0, 0, force_down, 0, 0, 0]
    force_type = 2
    limits = [2] * 6  # [1, 1, 1, 1, 1, 1]

    go_on_at = 0.9 * force_down  # 80%

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

force_drive(0.15, 0.3, 0.6)

rock_start_pos[2] = 0.45
rtde_c.moveP(rock_start_pos, 0.6, 2, 0.0)

# Wiggel

q_pose = rtde_r.getActualQ()

q_pose[-1] -= math.radians(25)
rtde_c.moveJ(q_pose, 0.6, 2, 0.0)

q_pose[-1] += math.radians(25)
rtde_c.moveJ(q_pose, 0.6, 3, 0.0)

q_pose[-3] -= math.radians(40)
rtde_c.moveJ(q_pose, 0.6, 3, 0.0)

q_pose[0] -= math.radians(60)
rtde_c.moveJ(q_pose, 0.85, 3, 0.0)

q_pose[-3] += math.radians(40)
rtde_c.moveJ(q_pose, 0.6, 3, 0.0)

# ------------------------------

force_drive(0.15, 0.40, 0.6)

rtde_c.moveP(fist_pose, 0.6, 2, 0.0)

rtde_c.stopScript()

run_id = str(uuid.uuid4())
np.save(f"{run_id}_pose.npy", pose_hist)
np.save(f"{run_id}_force.npy", force_hist)

plot_value_hist(pose_hist, name_mode="pose")
plot_value_hist(force_hist, name_mode="force")
