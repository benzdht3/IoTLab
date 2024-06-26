import serial.tools.list_ports
import time
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return "COM3"
if getPort() != None:
    ser = serial.Serial(port=getPort(), baudrate=115200)
    print(ser)

mess = ""
def processData(client,data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "T":
        client.publish("sensor1", splitData[2])
    if splitData[1] == "L":
        client.publish("sensor2", splitData[2])
    if splitData[1] == "H":
        client.publish("sensor3", splitData[2])
    if splitData[1] == "B":
        client.publish("button1", splitData[2])
    if splitData[1] == "P":
        client.publish("button2", splitData[2])
    

mess = ""
def readSerial(client):
    try:
        bytesToRead = ser.inWaiting()
        if (bytesToRead > 0):
            global mess
            mess = mess + ser.read(bytesToRead).decode("UTF-8")
            print(mess)
            while ("#" in mess) and ("!" in mess):
                start = mess.find("!")
                end = mess.find("#")
                processData(client, mess[start:end + 1])
                time.sleep(0.5)
                if (end == len(mess)):
                    mess = ""
                else:
                    mess = mess[end+1:]
    except KeyboardInterrupt:
        client.publish("Ack","2")
        time.sleep(2)

def writeData(data):
    ser.write(str(data).encode("utf-8"))
