import socket
import struct 
import time

MINE = "10.1.137.17"

UDP_PORT = 10001
FORMAT = 'BiBBBBBf'

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((MINE, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	var = struct.unpack(FORMAT,data)
	t = var[1]
	t = time.ctime(t)
	packAck=struct.pack('BBBBB',var[0],var[2],0,0, var[5]) 
	sock.sendto(packAck, (addr))
	print ("received message:", var[0], t, var[2], var[3], var[4] )
