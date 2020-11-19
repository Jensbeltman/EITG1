import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

motor = RpiMotorLib.A4988Nema(20, 16, (19,26,21), "A4988")

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    print(GPIO.input(6), GPIO.input(4))
    if GPIO.input(6):
        motor.motor_go(True, "Full", 1, .005, False, .05)
    elif GPIO.input(4):
        motor.motor_go(False, "Full", 1, .005, False, .05)



