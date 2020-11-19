import socket


class FunctionCallSendSocket(socket.socket):
    def __init__(self, HOST, PORT):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((HOST, PORT))

    @staticmethod
    def msg_format(l):
        return bytearray(' '.join(map(str, l)), "utf8")

    def motor_go(self, clockwise=False, steptype="Full", steps=200, stepdelay=.005, verbose=False, initdelay=.05):
        self.sendall(self.msg_format(["motor_go", clockwise, steptype, steps, stepdelay, verbose, initdelay]))

    def motor_go_to_endswitch(self, endswith="open", clockwise=False, steptype="Full", steps=5, stepdelay=.005, verbose=False, initdelay=.05):
        self.sendall(self.msg_format(["motor_go_to_endswitch", endswith, clockwise, steptype, steps, stepdelay, verbose, initdelay]))