import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

class EndSwith:
    def __init__(self, input_pin, name="", print_on_siwth=True):
        self._input_pin = input_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self._on = False

    def switch_down(self):
        is_down = GPIO.input(self._input_pin)
        if not self._on and is_down:
            self._on = True
            print_on_siwth
        return is_down


if __name__ == '__main__':
    motor = RpiMotorLib.A4988Nema(20, 16, (19,26,21), "A4988")

    GPIO.setmode(GPIO.BCM)

    end1 = EndSwith(4)
    end2 = EndSwith(6)

    while True:
        print(end1.switch_down(), end2.switch_down())
        if end1.switch_down():
            motor.motor_go(True, "Full", 1, .005, False, .05)
        elif end2.switch_down():
            motor.motor_go(False, "Full", 1, .005, False, .05)



