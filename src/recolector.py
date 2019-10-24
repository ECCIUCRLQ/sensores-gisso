import socket
import struct 
import time
import threading 
from ipcqueue import sysvmq # Biblioteca para los buzones.


MINE = "10.1.137.17"

UDP_PORT = 10001
FORMAT = 'BIBBBBBf'
ListaIdGrupo=["Whitenoise","FlamingoBlack","GISSO","KOF","Equipo 404","Poffis"]
listaSensores=["KeepAlive","Movimiento","Sonido","Luz","Shock","Touch","Humedad","BigSound","Temperatura","Ultrasonico"]
diccionario = {}

def crearThread(identificador):
	
	x = threading.Thread(target=correr, args=(identificador,))
	buz =sysvmq.Queue(identificador)	#crea buzon 
	diccionario.setdefault(identificador,buz) # z=key del buzon
	x.start()
	
def correr(nombre):
	buzComun = sysvmq.Queue(420)
	sid = nombre #Identificador
	#print("Corriendo: " + str(sid))
	buz =sysvmq.Queue(nombre)	#crea buzon 
	while True:
		print(nombre)
		#time.sleep(2)
		pack = buz.get()
		print (pack)
		#info = struct.unpack('BIBBBBBf',pack)
		
		if( pack[2]== 5 and (pack[6] == 6 or pack[6] == 8) ):	
			tipoDato = 2 #Tipo dato 2 es flotante
			infoUtil = struct.pack('IIfB',sid,pack[1],pack[7],tipoDato)
			buzComun.put(infoUtil)
		
		elif ( pack[2] == 6):
			tipoDato = 1 #Tipo dato 1 es entero
			infoUtil = struct.pack('IIfB',sid,pack[1],pack[7],tipoDato)
			buzComun.put(infoUtil)
		
		else:
			tipoDato = 0 #Tipo dato 0 es booleano
			infoUtil = struct.pack('IIfB',sid,pack[1],pack[7],tipoDato)
			buzComun.put(infoUtil)
			
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
	
	aEscribir = "Mensaje recibido de: " + ListaIdGrupo[var[2]-1] +"\n"+"Sensor: "+listaSensores[var[6]]+"\n"+"Numero Ack: "+str(var[0])+"\n"+"Fecha: " +str(t)+"\n"+"Dato: " +str(var[7])+"\n-------------------\n"
	print(aEscribir)	
	
	if(diccionario.get(identificador)== None):
		crearThread(identificador)
	
	else:
		diccionario.get(identificador).put(var)
		
	
