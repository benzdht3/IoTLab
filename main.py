from pickle import GLOBAL
import sys
import time
import random
from Adafruit_IO import MQTTClient
from uart import *
#from simpleAI import *

AIO_FEED_IDs = ["button1","button2","sensor1","sensor2","sensor3","ai","Ack"]
AIO_USERNAME = "benzdht"
AIO_KEY = "aio_kCcI29RhWiKcZHBsoYLvD3mXbBKk"

def connected(client):
    print("Connected ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)
    client.publish("Ack","0")


def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe successfully ...")

def disconnected(client):
    print("Disconnected ...")
    client.publish("Ack","2")
    sys.exit(1)

def message(client , feed_id , payload):
    print("Receive data: " + payload, feed_id)
    if feed_id == "Ack":
        if payload == "0.5":
            client.publish("Ack","0")
    if feed_id == "button1":
        client.publish("Ack","1")
        if payload == '1':
            writeData("Light Bulb is turned On\n")
        elif payload == '0':
            writeData("Light Bulb is turned OFF\n")
    if feed_id == 'button2':
        client.publish("Ack","1")
        if payload == '1':
            writeData("Pump is turned ON\n")
        elif payload == '0':
            writeData("Pump is turned OFF\n")



        

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
counter_ai = 10
ai_res = ""
prev_ai_res = ""
typ = random.randint(0,4)
try:
    while True:
    #pas ,image = camera.read()
    #image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    #cv2.imshow("Webcam", image)
    #client.publish("Ack","1")
        """if counter <= 0:
            counter = 10
            if typ == 0:
                temp = random.randint(15,60)
                client.publish("sensor1",temp)
            elif typ == 1:
                light = random.randint(0,500)
                client.publish("sensor2",light)
            elif typ == 2:
                humi = random.randint(0,100)
                client.publish("sensor3",humi)
            elif typ == 3:
                bulb = random.randint(0,1)
                client.publish("button1",bulb)
            else:
                pump = random.randint(0,1)
                client.publish("button2",pump)
            typ = random.randint(0,4) 
        counter_ai-=1
        if counter_ai <= 0:
            ai_res = ai_detect()
            if ai_res != prev_ai_res:
                #print(ai_res)
                prev_ai_res=ai_res
                client.publish("ai",ai_res)
            counter_ai=10"""
        readSerial(client)
     # Listen to the keyboard for presses.
        """try:
            keyboard_input = input()
    # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 'a':
                ser.write("a".encode("utf-8"))
            else:
                client.publish("Ack","2")
                disconnected(client)
        except KeyboardInterrupt:
            client.publish("Ack","2")
            time.sleep(2)"""
except KeyboardInterrupt:
    client.publish("Ack","2")
    time.sleep(2)