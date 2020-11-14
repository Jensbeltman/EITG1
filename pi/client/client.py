#!/usr/bin/env python3

import socket
import time




HOST = '10.0.0.3'  # The server's hostname or IP address
PORT = 65432        # The port used by the server



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall(b"True, Full , 200, .005, False, .05")

time.sleep(5)

s.sendall(b"False, Full , 200, .005, False, .05")

s.close()