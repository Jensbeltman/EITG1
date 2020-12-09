import rtde_receive
import rtde_control

robot_ip = "192.168.100.2"
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
rtde_c = rtde_control.RTDEControlInterface(robot_ip)

def go_to_next():
    anw = input("Go to next [y]:")
    if anw == "y":
        return
    else:
        exit()

speed = 0.25
acc = 1

go_to_next()

fist_pose = [-0.24126775044997928, -0.42075908202903856, 0.6586334885483427, 2.599420154499895, 0.09288735719897556, -0.6802083104833498]
rtde_c.moveP(fist_pose, speed, acc, 0.0)

go_to_next()

overRockwool_pos = [-0.08203968530815126, -0.5326926026406975, 0.3, -3.0392028741044914, -0.7231190853395795, -0.024991325114571333]
rtde_c.moveP(overRockwool_pos, speed, acc, 0.0)

go_to_next()

overRockwool_pos[2] = 0.15
rtde_c.moveP(overRockwool_pos, speed, acc, 0.0)

overRockwool_pos[2] = 0.45
rtde_c.moveP(overRockwool_pos, speed, acc, 0.0)

