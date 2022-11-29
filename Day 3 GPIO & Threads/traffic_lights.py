import RPi.GPIO as GPIO
import time
import random
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

green = 3
red = 2
signal = 4
button = 26
state_id = 0
button_pressed = False

def initial_state():
    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(signal, GPIO.OUT)
    GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
    GPIO.output(red, 0)
    GPIO.output(green, 0)
    GPIO.output(signal, 0)

def light_on(light):
    GPIO.output(light, 1)

def light_off(light):
    GPIO.output(light, 0)

def blink_light(light, time_range):
    for i in range(time_range):
        light_off(light)
        time.sleep(0.5)
        light_on(light)
        time.sleep(0.5)
    

class lightThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def light_fsm(self):
        global state_id
        global button_pressed
        button_pressed = False
        state_id = 1
        light_on(green)
        time.sleep(5)
        state_id = 2
        blink_light(green, 3)
        light_off(green)
        light_on(red)
        start_time = time.time()
        state_id = 3
        while not button_pressed:
            pass
        end_time = time.time()
        interval = end_time - start_time
        light_on(signal)
        if (interval < 5):
            time.sleep(5 - interval)
        time.sleep(3)
        light_off(red)
        light_off(signal)
        
        

    def run(self):
        print ('Starting ' + self.name + ' for light fsm.')
        try:
            while True:
                self.light_fsm()
        except KeyboardInterrupt:
            print("Stopped")
        finally:
            initial_state()
            GPIO.cleanup()


class buttonThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def button_detection(self):
        if GPIO.input(button) == False:
            start_time = time.time()
            while (GPIO.input(button) == False):
                   pass
            end_time = time.time()
            interval = end_time - start_time
            return interval
            print('Left button pressed for ', interval)
        return 0

    def run(self):
        print ('Starting ' + self.name + ' for button detection.')
        global state_id
        global button_pressed
        try:
            while True:
                if state_id == 3 and self.button_detection() >= 0.5:
                    button_pressed = True
        except:
            print("Exception")
        finally:
            initial_state()
            GPIO.cleanup()
                    
      

if __name__ == '__main__':
    initial_state()
    thread2 = lightThread(2, "Thread-2")
    thread1 = buttonThread(1, "Thread-1")
    thread1.daemon = True
    thread2.daemon = True
    thread1.start()
    thread2.start()
        

