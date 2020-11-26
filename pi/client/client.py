import socket
import time
from function_call_send_socket import FunctionCallSendSocket
import subprocess

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

HOST = '192.168.43.44'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = FunctionCallSendSocket(HOST,PORT)

speed = 0.0005
steps = 100

#s.motor_go(True, "Full", steps, speed, False, .05)
#s.motor_go(False, "Full", steps, speed, False, .05)
#s.motor_go(True, "Full", steps, speed, False, .05)
#s.motor_go(False, "Full", steps, speed, False, .05)
#s.motor_go(True, "Full", steps, speed, False, .05)
#s.motor_go(False, "Full", steps, speed, False, .05)


while True:
    intext = input("Write cmd,args: ")
    #copy2clip(intext)
    cmd, *args = intext.split(",")
    print(cmd, args)
    if cmd == "stop":
        print("Stopping")
        break

    if cmd == "in":
        if args == []:
            steps = 50
        else:
            steps = args[0]
        s.motor_go(False, "Full", steps, speed, False, .05)
    if cmd == "out":
        if args == []:
            steps = 50
        else:
            steps = args[0]
        s.motor_go(True, "Full", steps, speed, False, .05)



#time.sleep(10)


#s.motor_go(True, "Full", 1000, speed, False, .05)

#s.motor_go_to_endswith(endswith="open", clockwise=False, steptype="Full", steps=500, stepdelay=speed, verbose=False, initdelay=.05)

#time.sleep(3)

#s.motor_go_to_endswith(endswith="any", clockwise=False, steptype="Full", steps=25, stepdelay=speed, verbose=False, initdelay=.05)

#s.run_switch_test(endswith="any")


s.close()