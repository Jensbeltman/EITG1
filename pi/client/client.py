import socket
import time
from function_call_send_socket import FunctionCallSendSocket

HOST = '10.0.0.3'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = FunctionCallSendSocket(HOST,PORT)

s.motor_go(True, "Full" , 200, .005, False, .05)

time.sleep(3)

s.motor_go(False, "Full" , 200, .005, False, .05)

s.close()