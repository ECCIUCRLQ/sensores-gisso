import socket
import struct 
import time
import threading 


MINE = "10.1.138.56"

UDP_PORT = 10001
FORMAT = 'BIBBBBBf'
ListaIdGrupo=["Whitenoise","FlamingoBlack","GISSO","KOF","Equipo 404","Poffis"]
listaSensores=["KeepAlive","Movimiento","Sonido","Luz","Shock","Touch","Humedad","BigSound","Temperatura","Ultrasonico"]
diccionario = {}

def crearThread(identificador):
	
	x = threading.Thread(target=correr, args=(identificador,))
	#buz =sysvmq.Queue(identificador)	crea buzon 
	buz = identificador
	diccionario.setdefault(identificador,buz) # z=key del buzon
	x.start()
	
def correr(nombre):
	sid = nombre
	print("Corriendo: " + str(sid))
	#buz =sysvmq.Queue(nombre)	crea buzon 
	while True:
		print(nombre)
		time.sleep(2)
		# ~ pack = buz.get()
		# ~ info = struct.unpack(FORMAT,pack)	
		# ~ infoUtil = struct.pack('BBf',nombre,info[1],info[7])
		#nuevo buzon.put(infoUtil)
		

sock = socket.socket(socket.AF_INET, # Creacion del socket
                     socket.SOCK_DGRAM) 
sock.bind((MINE, UDP_PORT))# Se establece la conexion



# var[0] - ACK
# var[1] - Fecha
# var[2] - Equipo
# var[3] - 0
# var[4] - 0
# var[5] - ID sensor
# var[6] - Tipo de sensor
# var[7] - Dato

while True:
	data, addr = sock.recvfrom(50) # buffer size
	var = struct.unpack(FORMAT,data) # Desempaqueta los datos recibidos
	t = var[1]	# Fecha que se detecto 
	t = time.ctime(t)	# Cambio de formato
	packAck=struct.pack('BBBBB',var[0],var[2],0,0, var[5]) # Empaquetamos el ACK, Equipo y SensorID que se recibieron y se lo enviamos al cliente, esto para verificar que se recibio el paquete debido 
	sock.sendto(packAck, (addr))	# Enviamos al cliente este paquete
	identificador = str(var[2]) + str(var[5])
	identificador = int(identificador)
	
	if(diccionario.get(identificador)== None):
		crearThread(identificador)
	
	else:
		diccionario.get(identificador).put(var)
		
	
