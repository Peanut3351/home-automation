#!/usr/bin/python3
import socket

def inttobytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def intfrombytes(xbytes):
    return int.from_bytes(xbytes, 'big')

TCP_IP = 'rmg'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = inttobytes(99015576)
#MESSAGE = text.encode(encoding = 'utf-8', errors = 'strict')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
i.bind(('10.3.2.2', 5005))
i.listen(2)
s.connect(('rmg', 5005))
s.send(MESSAGE)
print("Data sent.")
conn, addr = i.accept()
data = conn.recv(BUFFER_SIZE)
print(str(intfrombytes(data)))
s.close
i.close
