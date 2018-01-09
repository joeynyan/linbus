import RPi.GPIO as GPIO
import time

Button = 18

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button():
    while True:
        input_state = GPIO.input(Button)
        if input_state == False:
            print('Button Pressed')
            time.sleep(0.2)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        button()
    except KeyboardInterrupt:
        destroy()
