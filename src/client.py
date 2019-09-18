import socket				
import struct				# struct usado para empaquetar los datos
import time			
import random	
import select
from ipcqueue import sysvmq # Biblioteca para los buzones.

UDP_IP = "10.1.137.9" 	#IP a enviar
MINE = "10.1.138.117"   # Mi ip, para el bind

UDP_PORT = 10001

SHOCK_ID = 0x04
MOV_ID = 0x01
KEEP_ALIVE = 0x0
TEAM_ID = 0x03
BOOL_TYPE = 0x01
FORMAT = 'BIBBBBBf'

shock =sysvmq.Queue(1)			# Se crea el buzon con la llave 1 para que se conecte con el creado en shock.py
mov = sysvmq.Queue(2)			# Se crea con la llave 2 para que se conecte con el creado en movement.py

lastRandomId = 0
randomId = -1

sock = socket.socket(socket.AF_INET, # Abrir los sockets
                     socket.SOCK_DGRAM) # 
sock.bind((MINE, UDP_PORT))	# Crea la conexion 

# Metodo que envia el paquete al cliente.
# Aqui se implementa el timeout, por lo tanto si el paquete se pierde,
# se reenvia cada 5 segundos.
def enviar(var):
	check = 0
	while check == 0 :
		sock.sendto(var, (UDP_IP, UDP_PORT))
		ready = select.select([sock], [], [], 5) #timeout de 5 segundos
		
		if ready[0]:
			data, addr = sock.recvfrom(50) # buffer size 
			ACK = struct.unpack('BBBBB', data)
			if randomId == ACK[0] :
				check = 1
				
# Metodo para generar random diferente al anterior
# Se usa para el ACK 
def getRandom():
	random1= random.randint(0,255)
	while(random1 == lastRandomId):
		random1 = random.randint(0,255) 
	return 	random1		
			
# Aqui se decide que enviar dependiendo de los datos que se reciben de los
# sensores.				
while True: 
	dateshock = -1
	try:	
		dateshock = shock.get_nowait() # get_nowait() revisa el buzon de shock, si esta vacio no pasa nada, y sino recibe el dato para enviarlo
	except:
		pass
		
	if dateshock == 0 :		# Entra cuando el sensor_shock envia un KeepAlive, es decir, no detecto nada
		randomId=getRandom()
		date = int(time.time())
		print ("Shock ",dateshock)
		packshock = struct.pack(FORMAT,randomId,date,TEAM_ID,0,0,2,KEEP_ALIVE,0.0)
		enviar(packshock)
		lastRandomId = randomId
	
	elif dateshock>0 : # Entra cuando el sensor_shock envia un dato, es decir, detecto shock.
		randomId=getRandom()
		print ("Shock ",dateshock)
		packshock = struct.pack(FORMAT,randomId,dateshock,TEAM_ID,0,0,2,SHOCK_ID,1.0)
		enviar(packshock)
		lastRandomId = randomId
		
	else:	# Si entra aqui, es porque el shock murio.
		pass
	
	datemov = -1
	try:
		datemov = mov.get_nowait() # Revisa el buzon de movimiento
	
	except:
		pass
		
	if datemov == 0 :	# Entra cuando el sensor_movement envia un KeepAlive, es decir, no detecto nada
		randomId=getRandom()
		date = int(time.time())
		print ("Mov ",datemov)
		packmov = struct.pack(FORMAT,randomId,date,TEAM_ID,0,0,1,KEEP_ALIVE,0)
		enviar(packmov)
		lastRandomId = randomId
	
	elif datemov>0: # Entra cuando el sensor_movement envia un dato, es decir, detecto shock. 
		randomId=getRandom()
		print ("Mov ",datemov)
		packmov = struct.pack(FORMAT,randomId,datemov,TEAM_ID,0,0,1,MOV_ID,1.0)
		enviar(packmov)
		lastRandomId = randomId
		
	else: # Si entra aqui, es porque el shock murio.
		pass	
	
	time.sleep(1)	# Espera el segundo y vuelve a enviar
