#!/usr/bin/python3
import RPI.GPIO as GPIO
import socket

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

def gettemp0():
    global i
    global tcp_port
    global lr_temp
    i.connect((lr_temp, tcp_port))
    message = inttobytes(98000101)
    i.send(message)
    i.close()
    return

def gettemp1():
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
    return

def sensors(x):
    sensorID = int(x[2:-4])
    cmdID = int(x[4:-2])
    cmdNo = int(x[6:])
    
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
    global temp
    typeID = x[:2]
    if typeID == '99':  #sending device is temp sensor
        sensors(x)
    if typeID == '00' or '01':  #sending device is desktop/laptop/mobile
        commands(x)

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
gettemp0()
gettemp1()

while 1:
    conn, addr = s.accept()
    data = conn.recv(buffer_size)
    decoded = str(intfrombytes(data))  #convert from bytes to numbers to string
    identify(decoded)  #break down the packet and conduct pertinent functions
