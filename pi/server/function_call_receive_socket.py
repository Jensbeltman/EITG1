import socket
from RpiMotorLib import RpiMotorLib

class FunctionCallReceiveSocket(socket.socket):
    def __init__(self, HOST, PORT, direction_pin, step_pin, mode_pins, motor_type="A4988"):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        # Function dict/map
        self.function = {"motor_go" : self.motor_go}
        
        #Motor setup
        self.motor = RpiMotorLib.A4988Nema(direction_pin, step_pin, mode_pins, "A4988")

        # Setup socket and start listen

        print("FunctionCallReceiveSocket started with HOST {} and PORT {}".format(HOST,PORT))
        self.bind((HOST, PORT))
        self.connection = None
        self.address = None
        self.wait_for_connection()
        self.wait_for_function_call()
    
    def wait_for_connection(self):
        self.listen()
        self.connection, self.address = self.accept()
        print("Connected to {}".format(self.address))

    def wait_for_function_call(self):
        while True:
            data = self.connection.recv(1024)
            data = repr(data)[2:-1].split(' ')

            if(data[0]==''):
                print("Connection with {} ended waiting for new one".format(self.address))
                self.wait_for_connection()
            else:
                print("Calling {} with parameters {}".format(data[0],data[1:]))
                self.function[data[0]](data[1:])

    def motor_go(self, data):
        self.motor.motor_go(data[0]=="True",data[1] , int(data[2]), float(data[3]), data[4]=="True", float(data[5]))
        