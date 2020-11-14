import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
    
#define GPIO pins
GPIO_pins = (19, 26, 21) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20       # Direction -> GPIO Pin
step = 16      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")


# call the function, pass the arguments
mymotortest.motor_go(True, "Full" , 200, .005, False, .05)

# good practise to cleanup GPIO at some point before exit
GPIO.cleanup()
