#!/usr/bin/python3
import socket

def get_ip():  #gets the IP of the hub device
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

def inttobytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def intfrombytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def tempsensor(x):  #decodes data packet from the temp sensor and sends it to the thermostat
    devID = int(x[2:-4])
    cmdID = int(x[4:-2])
    cmdNo = int(x[6:])
    global i
    global tcp_port
    i.connect(('raspberrypi', tcp_port))
    message = inttobytes(devID + cmdID + cmdNo)
    i.send(message)
    return

def thermostat(x)  #decodes data packet from the thermostat
    #TODO figure out what to do with this data
    return

def identify(x):
    typeID = x[:2]
    if typeID == '99':  #sending device is temp sensor
        tempsensor(x)
    if typeID == '98':  #sending device is thermostat
        thermostat(x)
    if typeID == '00':  #sending device is desktop/laptop
        desktop(x)
    if typeID == '01':  #sending device is mobile device (phone, tablet)
        mobile(x)
    return

tcp_ip = get_ip()   #sets bind IP to the IP of the device
tcp_port = 5005
buffer_size = 1024

i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((tcp_ip, tcp_port))
s.listen(1)     #open for tcp packet listening

while 1:
    conn, addr = s.accept()
    data = conn.recv(buffer_size)
    decoded = str(intfrombytes(data))   #convert from bytes to numbers to string
    identify(decoded)   #break down the packet and conduct pertinent functions
    print(decoded)
print("Exited loop")
s.shutdown(socket.SHUT_RDWR)
s.close()
exit()
