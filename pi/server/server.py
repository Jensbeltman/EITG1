import socket
import RPi.GPIO as GPIO

# import listen socket
from function_call_receive_socket import FunctionCallReceiveSocket

s = FunctionCallReceiveSocket(HOST = '192.168.43.44', PORT = 65432, direction_pin=20, step_pin=16, mode_pins=(19,26,21))