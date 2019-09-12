import socket
import struct
import time
import random

UDP_IP = "10.1.138.31" #IP a enviar
MINE = "10.1.137.32"   # Mi ip, para el bind

UDP_PORT = 10001

SHOCK_ID = 0x04
MOV_ID = 0x01
KEEP_ALIVE = 0x0
TEAM_ID = 0x03
BOOL_TYPE = 0x01
FORMAT = 'BiBBBBBf'
lastRandomId = 0
date = int( time.time() )
sensorId = SHOCK_ID
code = KEEP_ALIVE
data = True

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((MINE, UDP_PORT))
ListaIdGrupo=["Whitenoise","FlamingoBlack","GISSO","kof","Equipo404","Poffis"]
listaSensores=["KeepAlive","Movimiento","BigSound","Luz","Shock","Touch","Humedad","BigSound","Temperatura"]
for i in range (0,100):
	randomId= random.randint(0,255)
	while(randomId == lastRandomId):
		randomId = random.randint(0,255)	

	var = struct.pack(FORMAT,randomId,date,TEAM_ID,0,0,sensorId,code,data) 	

	sock.sendto(var, (UDP_IP, UDP_PORT))

	dataACK, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	ACK = struct.unpack('BBBBB', dataACK)
	if randomId == ACK[0] :
		print ("Mensaje enviado y recibido correctamente")
	else :
		print ("Mensaje enviado y recibido incorrectamente")
	
	
	
	
	print ( "received message:", ACK[0], ACK[1] )

	lastRandomId = ACK[0]
