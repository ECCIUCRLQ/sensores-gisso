import socket
import struct 
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	var = struct.unpack('iiii?',data)
	t = var[1]
	t = time.ctime(t)
	packAck=struct.pack('ii',var[0],var[2]) 
	sock.sendto(packAck, (UDP_IP, UDP_PORT))
	print "received message:", var[0], t, var[2], var[3], var[4]
