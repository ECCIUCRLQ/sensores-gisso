import socket
import struct
import time
import random

UDP_IP = "10.1.138.73"
UDP_PORT = 65432
SHOCK_ID = 0x04
MOV_ID = 0x01
KEEP_ALIVE = 0x0
TEAM_ID = 0x03
BOOL_TYPE = 0x01


date = time.time()
randomId= random.randint(0,65536)
sensorId = 000
code = KEEP_ALIVE
data = True


var = struct.pack('iiii?',randomId,date,sensorId,code,data) 

#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", UDP_PORT))

sock.sendto(var, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
ACK = struct.unpack('ii', data)

if randomId == ACK[0] :
	print "Mensaje enviado y recibido correctamente"
else :
	print "Mensaje enviado y recibido incorrectamente"

print "received message:", ACK[0], ACK[1]
