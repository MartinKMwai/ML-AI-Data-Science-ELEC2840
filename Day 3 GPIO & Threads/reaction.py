
import RPi.GPIO as GPIO
import time
import random
left_player = input('Left Player enter your name: ')
right_player = input('Right Player enter your name: ')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led = 4
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0)
t1=1
t2=5
time.sleep(random.uniform(t1,t2))
GPIO.output(led, 1)
left_button = 14
right_button = 15
#luck= random.choice([left_player,right_player])

GPIO.setup(left_button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(right_button, GPIO.IN, GPIO.PUD_UP)
#while True:
        #if GPIO.input(left_button) == False:
            #print(luck+" wins! ")
            #break
        #if GPIO.input(right_button) == False:
            #print(luck+" wins! ")
            #break       
try:
    while True:
        if GPIO.input(left_button) == False:
            print(left_player+" wins! ")
            break
        if GPIO.input(right_button) == False:
            print(right_player+" wins! ")
            break
    
except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    print("Cleaning up GPIO...")
    GPIO.cleanup()
