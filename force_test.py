import rtde_receive
import rtde_control
import time
import numpy as np
import matplotlib.pyplot as plt


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

home_q = [-1.1349614302264612, -1.2028576892665406, 2.1862648169146937, -2.5916811428465785, -1.6158507505999964, 1.9034147262573242]
#[-1.1562307516681116, -1.5013179343989869, 1.5410288015948694, -1.6028310261168421, -1.6128180662738245, 1.9432415962219238]
rtde_c.moveJ(home_q)

TCP_lower = [None, None, None, None, None, None]
#[None, None, 0.2484923468255163, None, None, None]

start_pose = rtde_r.getActualTCPPose()

speed = converter(1, "cm", "m")
acceleration = 0.5

pose_hist = []
force_hist = []

task_frame = start_pose
selection_vector = [0, 0, 1, 0, 0, 0]
wrench_up =        [0, 0, 10, 0, 0, 0]
force_type = 2
limits = [2]*6 #[1, 1, 1, 1, 1, 1]
dt = 1.0/500  # 2ms


# Execute 500Hz control loop for 4 seconds, each cycle is 2ms
for i in range(7000):
    start = time.time()
    # First move the robot down for 2 seconds, then up for 2 seconds

    rtde_c.forceMode(task_frame, selection_vector, wrench_up, force_type, limits)

    end = time.time()
    duration = end - start

    act_pose = rtde_r.getActualTCPPose()
    pose_hist.append(act_pose)
    force_hist.append(rtde_r.getActualTCPForce())

    if limet_check(act_pose, limetTCP_lower=TCP_lower):
        break

    if duration < dt:
        time.sleep(dt - duration)

rtde_c.forceModeStop()




rtde_c.stopScript()
plot_value_hist(pose_hist, name_mode="pose")
plot_value_hist(force_hist, name_mode="force")