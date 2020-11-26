import socket
import RPi.GPIO as GPIO

# import listen socket
from function_call_receive_socket import FunctionCallReceiveSocket

s = FunctionCallReceiveSocket(HOST = '192.168.43.44', PORT = 65433,
                              direction_pin=20, step_pin=16, mode_pins=(19,26,21),
                              endswitch_pin_closed=4, endswitch_pin_open=6)