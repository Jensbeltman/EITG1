#!/usr/bin/env python3

import socket
import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
    
#define GPIO pins
GPIO_pins = (19, 26, 21) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20       # Direction -> GPIO Pin
step = 16      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

HOST = '10.0.0.3'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            data_str = repr(data)
            dl = data_str[2:-1].replace(' ','').split(',')
            print('Received parameters ',data_str,dl)
            mymotortest.motor_go(bool(dl[0]),dl[1] , int(dl[2]), float(dl[3]), bool(dl[4]), float(dl[5]))

    