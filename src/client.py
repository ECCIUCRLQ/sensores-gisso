import socket
import struct
import time
import random
import select


UDP_IP = "10.1.138.31" #IP a enviar
MINE = "10.1.137.17"   # Mi ip, para el bind

UDP_PORT = 10001

SHOCK_ID = 0x04
MOV_ID = 0x01
KEEP_ALIVE = 0x0
TEAM_ID = 0x03
BOOL_TYPE = 0x01
FORMAT = 'BiBBBBBf'

date = int( time.time() )
randomId= random.randint(0,255)
sensorId = SHOCK_ID
code = KEEP_ALIVE
data = True

var = struct.pack(FORMAT,randomId,date,TEAM_ID,0,0,sensorId,code,data) 

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((MINE, UDP_PORT))
check = 0
contador = 0

while check == 0 and contador < 4:
	sock.sendto(var, (UDP_IP, UDP_PORT))


	ready = select.select([sock], [], [], 5) #timeout de 5 segundos
	
	if ready[0]:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		ACK = struct.unpack('BBBBB', data)
		
		if randomId == ACK[0] :
			print ("------RECIEVED-------\nACK Number Recieved =",ACK[0])
			print ("From =", ACK[1])
			print ("Sensor =", ACK[4])
			print ("--------------------------\n")
			check = 1
		else : #Recibio incorrecto
			print ("-------ERROR------")
			print ("Expected ACK =", randomId)
			print ("Recieved ACK =", ACK[0])
			print ("Re-sending...")
			print ("-------------\n")
			contador+=1
	else : #No recibio
		print ("-------------")
		print ("Missing ACK. Re-sending")
		print ("-------------\n")
		contador+=1

if check == 0 :
	print ("===============")
	print ("Conection lost")
	print ("===============")
