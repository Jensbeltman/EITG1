import socket
from RpiMotorLib import RpiMotorLib
from endSwith import EndSwith

class FunctionCallReceiveSocket(socket.socket):
    def __init__(self, HOST, PORT,
                 direction_pin, step_pin, mode_pins,
                 endswitch_pin_closed, endswitch_pin_open
                 ):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        # Function dict/map
        self.function = {"motor_go": self.motor_go,
                         "motor_go_to_endswith": self.motor_go_to_endswith}

        # Motor setup
        self.motor = RpiMotorLib.A4988Nema(direction_pin, step_pin, mode_pins, "A4988")

        # Endswith setup
        self.endswitch_open = None
        if endswitch_pin_open is not None:
            self.endswitch_open = EndSwith(endswitch_pin_open)

        self.endswitch_closed = None
        if endswitch_pin_closed is not None:
            self.endswitch_closed = EndSwith(endswitch_pin_closed)

        # Setup socket and start listen
        print("FunctionCallReceiveSocket started with HOST {} and PORT {}".format(HOST, PORT))
        self.bind((HOST, PORT))
        self.connection = None
        self.address = None
        self.wait_for_connection()
        self.wait_for_function_call()

    def wait_for_connection(self):
        self.listen()
        self.connection, self.address = self.accept()
        print("Connected to {}".format(self.address))

    def _decode_data(self, data):
        return repr(data)[2:-1].split(' ')

    def wait_for_function_call(self):
        while True:
            data = self.connection.recv(1024)
            print("Receved data:", data)
            data = self._decode_data(data)

            if (data[0] == ''):
                print("Connection with {} ended waiting for new one".format(self.address))
                self.wait_for_connection()
            else:
                print("Calling {} with parameters {}".format(data[0], data[1:]))
                self.function[data[0]](*data[1:])

    def motor_go(self, clockwise, steptype, steps, stepdelay, verbose, initdelay):
        """

        Parameters
        ----------
            clockwise: Diraction of the motor
            steptype: type of drive to step motor 5 options. (Full, Half, 1/4, 1/8, 1/16)
            steps: The number of steps to go between ceheeking the endswith
            stepdelay: Number of steps sequence's to execute. Default is one revolution , 200 in Full mode
            initdelay: Intial delay after GPIO pins initialized but before motor is moved
        """
        self.motor.motor_go(clockwise == "True",steptype, int(steps), float(stepdelay), verbose == "True", float(initdelay))

    def motor_go_to_endswith(self, endswith, clockwise, steptype, steps, stepdelay, verbose, initdelay):
        """
        Runs the motor with the given parameters until the endswith in meet.

        Parameters
        ----------
            endswith: Wich endswith to watch (open, closed)
            clockwise: Diraction of the motor
            steptype: type of drive to step motor 5 options. (Full, Half, 1/4, 1/8, 1/16)
            steps: The number of steps to go between ceheeking the endswith
            stepdelay: Number of steps sequence's to execute. Default is one revolution , 200 in Full mode
            initdelay: Intial delay after GPIO pins initialized but before motor is moved
        """
        end_switch_to_use = self.endswitch_open
        if endswith == "closed":
            end_switch_to_use = self.endswitch_closed

        if end_switch_to_use is None:
            print("The endswitch is not setup")
            return

        while not end_switch_to_use.switch_down():
            self.motor_go(clockwise, steptype, steps, stepdelay, verbose, initdelay)
