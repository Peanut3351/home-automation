#!/usr/bin/python3
import RPI.GPIO as GPIO
import socket
import sched
import time

lr_temp = 'raspberrypi'  #livingroom temp sensor hostname/IP
br_temp = ''  #bedroom temp sensor hostname/IP
temp0 = null  #living room temp
temp1 = null  #bedroom temp
target_temp = 76
W1 = 22  #heat 1st stage
W2 = null  #heat 2nd stage
Y1 = 27  #compressor 1st stage
Y2 = null  #compressor 2nd stage
G = 17  #fan
config = open("config.txt", "rw")

def get_ip():  #gets the IP of the current device
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    return IP

def requestTemp0():
    global i
    global tcp_port
    global lr_temp
    i.connect((lr_temp, tcp_port))
    message = inttobytes(98000101)
    i.send(message)
    i.close()
    return

def requestTemp1():
    global i
    global tcp_port
    global br_temp
    i.connect((br_temp, tcp_port))
    message = inttobytes(98000101)
    i.send(message)
    i.close()
    return

def intfrombytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def inttobytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def commands(x):
    deviceID = x[2:-4]
    cmdType = x[4:-2]
    cmdValue = x[6:]
    return

def sensors(x):
    global temp0
    global temp1
    sensorID = x[2:-4]
    dataType = x[4:-2]
    dataValue = x[6:]
    if sensorID == '02':
        temp0 = dataValue
    if sensorID == '03':
        temp1 = dataValue
    return

def allOff():  #open all relays
    GPIO.output([W1,Y1,G], 1)
    return

def heatOn():  #turn on heat
    allOff()
    GPIO.output(W1, 0)
    GPIO.output([Y1,G], 1)
    return

def acOn():  #turn on compressor and fan
    allOff()
    GPIO.output([Y1,G], 0)
    GPIO.output(W1, 1)
    return

def identify(x):
    typeID = x[:2]
    if typeID == '99':  #sending device is temp sensor
        sensors(x)
    if typeID == '00' or '01':  #sending device is desktop/laptop/mobile
        commands(x)
    return

def process(conn):
    global buffer_size
    data = conn.recv(buffer_size)
    decoded = str(intfrombytes(data))  #convert from bytes to numbers to string
    return decoded

def preferredSens():
    global config
    global temp0
    global temp1
    preferred = config.readline(1)
    if preferred == '0':
        return temp0
    if preferred == '1':
        return temp1
    return

def systemRun():
    global target_temp
    if preferredSens() > target_temp and mode() == 'aircon':
        acOn()
    if preferredSens() <= target_temp and mode() == 'aircon':
        allOff()
    if preferredSens() < target_temp and mode() == 'heat':
        heatOn()
    if preferredSens() >= target_temp and mode() == 'heat':
        allOff()
    return



GPIO.setmode(GPIO.BCM)
outputs = [22,27,17]
GPIO.setup(outputs, GPIO.OUT)

tcp_ip = get_ip()  #sets bind IP to the IP of the device
tcp_port == 5005
buffer_size = 1024

i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((tcp_ip, tcp_port))
s.listen(1)  #open for tcp packet listening

conn = null
addr = null
starttime = time.time()
while 1:
    requestTemp0()
    conn, addr = s.accept()
    identify(process(conn))
    s.close()
#    requestTemp1()
#    conn, addr = s.accept()
#    identify(process(conn))
#    s.close()
    systemRun()
    time.sleep(60 - ((time.time() - starttime) % 60.0))
