import socket
import time
from function_call_send_socket import FunctionCallSendSocket

HOST = '192.168.43.44'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = FunctionCallSendSocket(HOST,PORT)

speed = 0.0005

s.motor_go(True, "Full", 1000, speed, False, .05)

time.sleep(3)

s.motor_go(True, "Full", 1000, speed, False, .05)

#s.motor_go_to_endswith(endswith="open", clockwise=False, steptype="Full", steps=5, stepdelay=.005, verbose=False, initdelay=.05)

#time.sleep(3)

#s.motor_go_to_endswith(endswith="closed", clockwise=False, steptype="Full", steps=25, stepdelay=speed, verbose=False, initdelay=.05)

s.close()