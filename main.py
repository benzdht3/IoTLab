import sys
import time
import random
from Adafruit_IO import MQTTClient
from uart import *
from simpleAI import *

AIO_FEED_IDs = ["button1","button2","sensor1","sensor2","sensor3","ai"]
AIO_USERNAME = "benzdht"
AIO_KEY = "aio_KcLG56r8M3GA9owxG4oBZUElPXDl"

def connected(client):
    print("Connected ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe successfully ...")

def disconnected(client):
    print("Disconnected ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Receive data: " + payload, feed_id)
    if feed_id == "button1":
        if payload == '1':
            writeData(1)
        else:
            writeData(2)
    elif feed_id == "button2":
        if payload == '1':
            writeData(3)
        else:
            writeData(4)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter_ai = 10
ai_res = ""
prev_ai_res = ""
typ = random.randint(0,4)
while True:
    #counter = counter -1
    #if counter <= 0:
        #counter = 10
        #if typ == 0:
        #    temp = random.randint(15,60)
        #    client.publish("sensor1",temp)
        #elif typ == 1:
        #    light = random.randint(0,500)
        #    client.publish("sensor2",light)
        #elif typ == 2:
        #    humi = random.randint(0,100)
        #    client.publish("sensor3",humi)
        #elif typ == 3:
        #    bulb = random.randint(0,1)
        #    client.publish("button1",bulb)
        #else:
        #    pump = random.randint(0,1)
        #    client.publish("button2",pump)
        #typ = random.randint(0,4) 
    counter_ai-=1
    if counter_ai <= 0:
        ai_res = ai_detect()
        if ai_res != prev_ai_res:
            #print(ai_res)
            prev_ai_res=ai_res
            client.publish("ai",ai_res)
        counter_ai=10
    readSerial(client)
     # Listen to the keyboard for presses.

    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
    time.sleep(0.5)
    pass