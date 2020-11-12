import rtde_receive

robot_ip = "192.168.100.2"
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)

print("getActualQ", rtde_r.getActualQ())
print("getActualTCPPose", rtde_r.getActualTCPPose())
print("getActualTCPForce", rtde_r.getActualTCPForce())
