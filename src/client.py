import socket
import struct
import time
import random

UDP_IP = "10.1.137.79"
MINE = "10.1.137.17"
UDP_PORT = 10002

SHOCK_ID = 0x04
MOV_ID = 0x01
KEEP_ALIVE = 0x0
TEAM_ID = 0x03
BOOL_TYPE = 0x01

date = int( time.time() )
randomId= random.randint(0,255)
sensorId = 000
code = KEEP_ALIVE
data = True


var = struct.pack('BiiB?',randomId,date,sensorId,code,data) 

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((MINE, UDP_PORT))

sock.sendto(var, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
ACK = struct.unpack('ii', data)

if randomId == ACK[0] :
	print ("Mensaje enviado y recibido correctamente")
else :
	print ("Mensaje enviado y recibido incorrectamente")

print ( "received message:", ACK[0], ACK[1] )
