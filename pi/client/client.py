import socket
import time
from function_call_send_socket import FunctionCallSendSocket

HOST = '192.168.43.44'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = FunctionCallSendSocket(HOST,PORT)

speed = 0.0005
steps = 600

#s.motor_go(True, "Full", steps, speed, False, .05)
#s.motor_go(False, "Full", steps, speed, False, .05)
#s.motor_go(True, "Full", steps, speed, False, .05)
#s.motor_go(False, "Full", steps, speed, False, .05)
#s.motor_go(True, "Full", steps, speed, False, .05)
#s.motor_go(False, "Full", steps, speed, False, .05)

#time.sleep(10)


#s.motor_go(True, "Full", 1000, speed, False, .05)

#s.motor_go_to_endswith(endswith="open", clockwise=False, steptype="Full", steps=500, stepdelay=speed, verbose=False, initdelay=.05)

#time.sleep(3)

#s.motor_go_to_endswith(endswith="any", clockwise=False, steptype="Full", steps=25, stepdelay=speed, verbose=False, initdelay=.05)

s.run_switch_test(endswith="any")


s.close()