import rtde_receive
import rtde_control

robot_ip = "192.168.100.2"
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
rtde_c = rtde_control.RTDEControlInterface(robot_ip)

start_pose = rtde_r.getActualTCPPose()
print("Start pose is {}".format(start_pose))

print(type(start_pose))
pose = list(start_pose)


speed = 0.5
acceleration = 0.5


current_frame = rtde_r.getActualTCPPose()
rtde_c.forceMode(current_frame, [0,0,1,0,0,0], [0,0,0,0,0,0], 1, [0,0,10,0,0,0])
teachModeActive = rtde_c.teachMode()
print(teachModeActive)
text = input("Press to step teach mode")
teachModeActive = rtde_c.endTeachMode()
print(teachModeActive)
