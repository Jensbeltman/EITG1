import RPi.GPIO as GPIO

# GPIO6, GPIO5

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN)

while True:
    print(GPIO.input(5), GPIO.input(6))

