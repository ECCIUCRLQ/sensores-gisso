import sys
import socket
import threading
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

BUFFER_SIZE = 692000
PORT_NM_ID = 5000

sendBcast = 0

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
	
	elif(tamanoDisponible < 17):
		tamanoDisponible = 0

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
	tamDisponible()
	
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
			archivo.seek(indice+13)
			fecha = int(time.time())
			archivo.write(fecha.to_bytes(4,byteorder = 'big'))
			archivo.seek(inicioDatos)
			datosCompletos = archivo.read(tam)
			
		else:
			indice += 17
	
	return datosCompletos
			
def broadcast():
	global tamanoDisponible
	global sendBcast
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	server_address = ('10.1.255.255', PORT_NM_ID)

	paqueteBcast = struct.pack('=BI',5,tamanoDisponible)
	try:
		while sendBcast == 0:
			sock.sendto(paqueteBcast, server_address)
			print('Soy nodo deme pelota')
			
			time.sleep(1)	
	finally:	
		sock.close()
		print("Termino Bcast")
	
def recibirTCP():
	global sendBcast
	global tamanoDisponible
	
	PORT = 3114        # Port to listen on (non-privileged ports are > 1023)
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('', PORT))
		s.listen()
		while True:
			conn, addr = s.accept()
			print("Conectado a: ",addr)
			with conn:
				data = conn.recv(BUFFER_SIZE)
				# ~ opCode = int.from_bytes(data[0:1], byteorder = 'big')
				# ~ idPagina = int.from_bytes(data[1:2], byteorder = 'big')
				# ~ tamanio = int.from_bytes(data[2:5], byteorder = 'big')
				# ~ data = data[5:len(data)]
				
				opCode = struct.unpack("=B", data[0:1])[0]
				
				if(opCode == 0):
					print("Guardando")
					idPagina = struct.unpack("=B", data[1:2])[0]
					tamanio = struct.unpack("=I", data[2:6])[0]
					datos = data[6:]
					print("Datos ",datos)
					datosGuardar = (idPagina,tamanio,datos)
					agregarDatos(datosGuardar)
					mandar = struct.pack("=BBI",2,idPagina,tamanoDisponible)
					conn.sendall(mandar)
					print("Guardado, ",mandar)
					
				elif(opCode == 1):	
					print("Buscando")
					idPagina = struct.unpack("=B", data[1:2])[0]
					print("ID pagina ",idPagina)
					correcto = buscarDatos(idPagina)
					if(correcto != -1):
						correcto = struct.pack("=B",3)
						correcto = correcto + datos
						
					else:
						correcto = struct.pack("=B",4)
						
					conn.sendall(correcto)
					print("Buscado ",correcto)
				elif(opCode == 2):
					sendBcast = 1
					
				# ~ print(len(data))
				# ~ print("asssssssssssssssta: ", opCode)
				# ~ print("asssssssssssssssta: ", idPagina)
				# ~ print("asssssssssssssssta: ", tamanio)
				# ~ print("asssssssssssssssta: ", datos)
				# ~ #data = struct.unpack(FormatoTCP,data)
				# ~ print("Data: ", data)
				
				# ~ conn.sendall(data)
		
	s.close()

def comLs():
	global punteroMeta
	
	
	while True:
		commando = str(input())
		indice = 8
		if(commando == "ls"):
			archivo = open("nodoMemoria.bin", 'br')
			archivo.seek(punteroMeta)
			finMeta = int.from_bytes(archivo.read(4), byteorder = 'big')
			print("FechaCreacion\t\t\tFechaConsulta\t\t\tID\tTamano")
			while(indice < finMeta):
				archivo.seek(indice)
				identificador = int.from_bytes(archivo.read(1), byteorder = 'big')
				archivo.seek(indice+1)
				tam = int.from_bytes(archivo.read(4), byteorder = 'big')
				archivo.seek(indice+9)
				fechaCrea = int.from_bytes(archivo.read(4), byteorder = 'big')
				fechaCrea = time.ctime(fechaCrea)
				archivo.seek(indice+13)
				fechaCons = int.from_bytes(archivo.read(4), byteorder = 'big')
				fechaCons = time.ctime(fechaCons)
				print((fechaCrea)+"\t"+(fechaCons)+"\t"+str(identificador)+"\t"+str(tam))
				indice += 17
			archivo.seek(0)
			bina = archivo.read()
			print(bina)
			archivo.close()
		else:
			print("El comando no existe")
		
def init():
	crearArchivo()
	tamDisponible()
	threadBcast = threading.Thread(target=broadcast)
	threadBcast.start()
	threadLs = threading.Thread(target=comLs)
	threadLs.start()
	while True:
		recibirTCP()

init()
