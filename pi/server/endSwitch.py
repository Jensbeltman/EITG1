import RPi.GPIO as GPIO

# GPIO6, GPIO5

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    print(GPIO.input(6), GPIO.input(4))

