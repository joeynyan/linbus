import RPi.GPIO as GPIO
import time
import threading
import curses

LedPin = 11
Button = 12
ThreadNum = 0

def setup():
    GPIO.setmode(GPIO.BOARD) #numbers gpios by location
    GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LedPin, GPIO.OUT) # set ledPin's mode as output
    #GPIO.output(LedPin, GPIO.HIGH) #set ledpin high(+3.3V) to turn on

def blink():
    GPIO.output(LedPin, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(LedPin, GPIO.LOW)
    time.sleep(0.2)

def button(stdscr):
    stdscr.nodelay(1) #do not wait for input when calling getch
    blinkState = True
    ThreadNum = 0
    thread1 = myThread(ThreadNum, "thread1", blinkState)
    thread1.start()
    while True:
        input_state = GPIO.input(Button)
#        print('button check')
        if input_state == False:
            blinkState = not blinkState
            print(blinkState)
        c = stdscr.getch()
        if c == -1:
            if blinkState and thread1.isAlive():
#                print('set')
                thread1.setBlink()
            elif not blinkState and thread1.isAlive():
                thread1.stop()
        else:
            print('die')
            thread1.kill()
        stdscr.refresh()
        stdscr.move(0, 0)
        
           # ThreadNum = ThreadNum + 1
           # thread1 = myThread(ThreadNum, "hi", blinkState)
            
        time.sleep(0.3)

def destroy():
    GPIO.output(LedPin, GPIO.LOW)
    GPIO.cleanup()

class myThread (threading.Thread):
    def __init__(self, threadID, name, flag):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.flag = flag
        self.alive = True

    def run(self):
        print("Starting " + str(self.threadID))
        self.blinkblink()

    def setBlink(self):
        if not self.flag:
            self.flag = True
#            self.blinkblink()

    def stop(self):
        self.flag = False

    def blinkblink(self):
        while self.alive:
            if self.flag == True:
                blink()
    def kill(self):
        self.alive = False

if __name__ == '__main__':
    setup()
    try:
        curses.wrapper(button)
        #blink()
    except KeyboardInterrupt:
        print("exiting")
        destroy()
