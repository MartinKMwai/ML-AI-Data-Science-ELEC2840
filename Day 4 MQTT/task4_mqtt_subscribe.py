import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import random
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

hostname = "test.mosquitto.org"
port = 1883
topic1 = "PC000/traffic_light_state/state1"
topic2 = "PC000/traffic_light_state/state2"
topic3 = "PC000/traffic_light_state/state3"

green = 3
red = 2
signal = 4
state_id = 0
pressedbutton = False
disabledbutton = False
Emergency = True

def on_connect(client, userdata, flags, rc):
   # Successful connection is '0'
   print("[MQTT] Connection result: " + str(rc))
   if rc == 0:
        client.subscribe("PC000/traffic_light/emergency")

def on_publish(client, userdata, mid):
   print("[MQTT] Sent: " + str(mid))

def on_disconnect(client, userdata, rc):
   if rc != 0:
       print("[MQTT] Disconnected unexpectedly")
       
def on_message(client, userdata, message):
    global isEmergency
    isEmergency = message.payload.decode("utf-8") == "True"
    print (isEmergency)
    

# Initialize client instance
client = mqtt.Client()

# Bind events to functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.on_message = on_message


# Connect to the specified broker
client.connect(hostname, port=port)

# Network loop runs in the background to listen to the events
client.loop_start()


def publish_message(topic, state):
    client.publish(topic, state, qos=0, retain=False)

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
    

class MainThread ():
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def light_fsm(self):
        global state_id
        global button_pressed
        button_pressed = False
        state_id = 1
        publish_message(topic1, state_id)
        light_on(green)
        time.sleep(5)
        state_id = 2
        publish_message(topic2, state_id)
        blink_light(green, 3)
        light_off(green)
        light_on(red)
        start_time = time.time()
        state_id = 3
        publish_message(topic3, state_id)
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


class SignalLEDThread (threading.Thread):
    def run(self):
        global isEmergency
        global disable_button
        while True:
            while isEmergency:
                disable_button = True
                GPIO.output(signal, 1)
                time.sleep(0.5)
                GPIO.output(signal, 0)
                time.sleep(1)
            disable_button = False
    

class ButtonThread (threading.Thread):
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
                if state_id == 3 and self.button_detection() >= 0.5 and not disable_button:
                    button_pressed = True
        except:
            print("Exception")
        finally:
            initial_state()
            GPIO.cleanup()
                    
      

if __name__ == '__main__':
    initial_state()
    thread3 = SignalLEDThread()
    thread2 = MainThread(2, "Thread-2")
    thread1 = ButtonThread(1, "Thread-1")
    thread1.daemon = True
    thread3.daemon = True
    thread1.start()
    thread3.start()
    thread2.run()
    
        

