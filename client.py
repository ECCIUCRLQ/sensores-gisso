import socket
import struct
import time
import random

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
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
sock.sendto(var, (UDP_IP, UDP_PORT))
