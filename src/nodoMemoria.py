import sys
import socket
#from socket import *
import time
import struct
#Metadatos Generales:
#-Puntero final de metadatos 4 bytes
#-Puntero final de datos 4 bytes

#Metadatos de cada dato:
#-ID 1 bytes
#-Tamaño pagina 4 bytes
#-Puntero donde inician los datos 4 bytes
#-Fecha Modificacion 4 bytes
#-Fecha Consulta 4 bytes
punteroMeta = 0
punteroDatos = 4
IDIP = 0

if( len(sys.argv) < 2 ):
	print ("NodoMemoria: Error, argumentos insuficientes")
	exit()

tamanoMax = int(sys.argv[1])
tamanoDisponible = tamanoMax

def crearArchivo():
	global tamanoMax
	global punteroMeta
	global punteroDatos
	
	archivo = open("nodoMemoria.bin", 'bw')
	archivo.seek(punteroMeta)
	puntM = 8
	puntD = tamanoMax
	archivo.write(puntM.to_bytes(4,byteorder = 'big'))
	archivo.seek(punteroDatos)
	archivo.write(puntD.to_bytes(4,byteorder = 'big'))
	archivo.close()
	
def tamDisponible():
	global tamanoMax
	global tamanoDisponible
	
	if(tamanoMax == tamanoDisponible):
		tamanoDisponible -= 25
	
	else:
		tamanoDisponible -= 17
		
	return tamanoDisponible
	
def agregarMetadatos(idPagina,tamPagina):
	archivo = open("nodoMemoria.bin", 'br+')
	archivo.seek(punteroMeta)
	escribiendoMeta = int.from_bytes(archivo.read(4), byteorder = 'big')
	
	archivo.seek(punteroDatos)
	escribiendoDatos = int.from_bytes(archivo.read(4), byteorder = 'big')
	
	archivo.seek(escribiendoMeta)
	archivo.write(idPagina.to_bytes(1,byteorder = 'big'))
	archivo.write(tamPagina.to_bytes(4,byteorder = 'big'))
	
	escribiendoDatos -= tamPagina
	archivo.write(escribiendoDatos.to_bytes(4,byteorder = 'big'))
	
	fechaCreacion = int(time.time())
	archivo.write(fechaCreacion.to_bytes(4,byteorder = 'big'))
	archivo.write(fechaCreacion.to_bytes(4,byteorder = 'big'))
	
	escribiendoMeta += 17
	archivo.seek(punteroMeta)
	archivo.write(escribiendoMeta.to_bytes(4,byteorder = 'big'))
	archivo.seek(punteroDatos)
	archivo.write(escribiendoDatos.to_bytes(4,byteorder = 'big'))
	
	archivo.close()
	
	return escribiendoDatos
	
	
def agregarDatos(datos):
	global tamanoDisponible
	
	escribiendo = agregarMetadatos(datos[0],datos[1])
	archivo = open("nodoMemoria.bin", 'br+')
	archivo.seek(escribiendo)
	archivo.write(datos[2]) #####Aqui falta ver el formato de los datos y ver cuales guardar
	archivo.close()
	
	tamanoDisponible -= datos[1]
	
def buscarDatos(idPagina):
	global punteroMeta
	
	inicioDatos = -1
	indice = 8
	identificador = -1
	terminar = False
	datosCompletos = -1
	archivo = open("nodoMemoria.bin", 'br+')
	archivo.seek(punteroMeta)
	finMeta = int.from_bytes(archivo.read(4), byteorder = 'big')
	while(terminar == False and indice < finMeta):
		archivo.seek(indice)
		identificador = int.from_bytes(archivo.read(1), byteorder = 'big')
		if(identificador == idPagina):
			terminar = True
			archivo.seek(indice+1)
			tam = int.from_bytes(archivo.read(4), byteorder = 'big')
			archivo.seek(indice+5)
			inicioDatos = int.from_bytes(archivo.read(4), byteorder = 'big')
			archivo.seek(inicioDatos)
			datosCompletos = archivo.read(tam)
			
		else:
			indice += 17
	
	return datosCompletos
		
		
def broadcast():
	global IDIP
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	#sock.settimeout(5)
	sock.setblocking(0)

	server_address = ('255.255.255.255', 5000)
	message = 'pfg_ip_broadcast_cl'

	try:
		while True:
			# Send data
			#print('Ivanxd sending: ' + message)
			sent = sock.sendto(message.encode(), server_address)

			# Receive response
			#print('waiting to receive')
			try:
				data, server = sock.recvfrom(4096)
				if data.decode('UTF-8') == 'pfg_ip_response_serv':
					print('Received confirmation')
					IDIP = server[0]
					print('Server ip: ' + str(server[0]) )
					break
				else:
					print('Verification failed')
			except:
				print('Soy nodo deme pelota')
			time.sleep(2)	
	finally:	
		sock.close()
	
def recibirTCP():
	global IDIP
	  
	PORT = 3114        # Port to listen on (non-privileged ports are > 1023)
	print("hola")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(('10.1.138.93', PORT))
		print("hola22")
		s.listen()
		print("hola23")
		while True:
			conn, addr = s.accept()
			print("hola54")
			print(addr)
			with conn:
				print('Connected by', addr)
				data = conn.recv(1024)
				print("Data: ", data)
				
				conn.sendall(data)
		
	#socket.close(0)
def test():
	
	crearArchivo()
	broadcast()
	recibirTCP()
	# ~ datos = bytearray([0,2,3,4,5])
	# ~ datos1 = bytearray([1,2,3,4,5])
	# ~ datos2 = bytearray([2,2,3,4,5])
	# ~ formatoGuardar = "BBI" + str(len(datos)) +"s"
	# ~ formatoGuardar1 = "BBI" + str(len(datos1)) +"s"
	# ~ formatoGuardar2 = "BBI" + str(len(datos2)) +"s"
	# ~ pagID = 2
	# ~ tamPag = len(datos) # * 5 con este 5 lo mandan desde mem local
	
	# ~ print ("Len datos", len(datos))
	
	# ~ packGuardar = struct.pack(formatoGuardar,0,1,tamPag,datos)
	# ~ packGuardar1 = struct.pack(formatoGuardar1,0,2,tamPag,datos1)
	# ~ packGuardar2 = struct.pack(formatoGuardar2,0,3,tamPag,datos2)
	
	# ~ paquete = struct.unpack(formatoGuardar,packGuardar)
	# ~ paquete1 = struct.unpack(formatoGuardar1,packGuardar1)
	# ~ paquete2 = struct.unpack(formatoGuardar2,packGuardar2)
	
	# ~ paqueteQuiero = [paquete[1],paquete[2],paquete[3]]
	# ~ paqueteQuiero1 = [paquete1[1],paquete1[2],paquete1[3]]
	# ~ paqueteQuiero2 = [paquete2[1],paquete2[2],paquete2[3]]
	
	# ~ agregarDatos(paqueteQuiero)
	# ~ agregarDatos(paqueteQuiero1)
	# ~ agregarDatos(paqueteQuiero2)
	
	# ~ print ("Paquete Guarde:",datos)
	
	# ~ datosVuelta = buscarDatos(1)
	# ~ datosVuelta1 = buscarDatos(2)
	# ~ datosVuelta2 = buscarDatos(3)
	
	# ~ print ("Paquete pedi:", datosVuelta)
	# ~ print ("Paquete pedi:", datosVuelta1)
	# ~ print ("Paquete pedi:", datosVuelta2)


test()
