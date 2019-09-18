import socket
import struct
import time
import random
import select
from ipcqueue import sysvmq

UDP_IP = "10.1.138.139" #IP a enviar
MINE = "10.1.138.117"   # Mi ip, para el bind

UDP_PORT = 10001

SHOCK_ID = 0x04
MOV_ID = 0x01
KEEP_ALIVE = 0x0
TEAM_ID = 0x03
BOOL_TYPE = 0x01
FORMAT = 'BIBBBBBf'

shock =sysvmq.Queue(4)
mov = sysvmq.Queue(3)


sensorId = SHOCK_ID

lastRandomId = 0
randomId = -1



sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((MINE, UDP_PORT))

contador = 0

def enviar(var):
	check = 0
	while check == 0 :#and contador < 4:
		sock.sendto(var, (UDP_IP, UDP_PORT))


		ready = select.select([sock], [], [], 5) #timeout de 5 segundos
		
		if ready[0]:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
			ACK = struct.unpack('BBBBB', data)
			
			if randomId == ACK[0] :
				check = 1
				#print ("------RECIEVED-------\nACK Number Recieved =",ACK[0])
				#print ("From =", ACK[1])
				#print ("Sensor =", ACK[4])
				#print ("--------------------------\n")
				
def getRandom():
	randomId= random.randint(0,255)
	while(randomId == lastRandomId):
		randomId = random.randint(0,255) 			
				
while True: 
		
	dateshock = shock.get()
	if dateshock == 0 :
		getRandom()
		date = int(time.time())
		print ("Shock ",dateshock)
		packshock = struct.pack(FORMAT,randomId,date,TEAM_ID,0,0,2,KEEP_ALIVE,0.0)
		enviar(packshock)
		lastRandomId = randomId
	
	else: 
		getRandom()
		print ("Shock ",dateshock)
		packshock = struct.pack(FORMAT,randomId,dateshock,TEAM_ID,0,0,2,SHOCK_ID,1.0)
		enviar(packshock)
		lastRandomId = randomId
		
	
	datemov = mov.get()
	if datemov == 0 :
		getRandom()
		date = int(time.time())
		print ("Mov ",datemov)
		packmov = struct.pack(FORMAT,randomId,date,TEAM_ID,0,0,1,KEEP_ALIVE,0)
		enviar(packmov)
		lastRandomId = randomId
	
	else: 
		getRandom()
		print ("Mov ",datemov)
		packmov = struct.pack(FORMAT,randomId,datemov,TEAM_ID,0,0,1,MOV_ID,1.0)
		enviar(packmov)
		lastRandomId = randomId
		
	time.sleep(1)	
