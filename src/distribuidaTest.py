import os
import struct
import random
import socket
import time
import sys
import uuid 
import threading
  

MY_IP = '10.1.138.103'  # Mi IP
IP_Nodo = 0

formatoBcast = '=BI'
PUERTO_BC = 6000
PUERTO_CHAMPIONS = 6666
PORT_NM = 3114
BUFFER_SIZE = 691210

formato_champions = '=BIB'
ronda_champions = 0
soy_activa = False 
my_mac = 0


def crearPaquete(ID):
	datos = bytearray([0,2,3,4,5])
	formatoGuardar = "=BBI"
	tamPag = int(len(datos))
	packGuardar = struct.pack(formatoGuardar,0,ID,tamPag)
	packGuardar += datos
	
	return packGuardar

def crearPaquetePedir():
	formatoGuardar = "=BB"
	packpedir = struct.pack(formatoGuardar,1,1)
	return packpedir

def respuestaTCP(IP_Nodo):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		socket_send.connect((IP_Nodo, PORT_NM))
		paqueteRespuesta = struct.pack('=B',2)
		socket_send.sendall(paqueteRespuesta)
		socket_send.close()
		print ("Respondi por TCP")

def sendTCP(paquete, IP_Nodo):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		while True:
			try:
				socket_send.connect((IP_Nodo, PORT_NM))
				socket_send.sendall(paquete)
				data, address = socket_send.recvfrom(BUFFER_SIZE)
				if(data[0] == 2):
					print("Recibido correctamente")
					socket_send.close()
					break
					
			except:
				time.sleep(1)
				pass		
	
def pedirTCP(paquete, IP_Nodo):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_pedir:
		while True:
			try:
				socket_pedir.connect((IP_Nodo, PORT_NM))
				socket_pedir.sendall(paquete)
				data, address = socket_pedir.recvfrom(BUFFER_SIZE)
				if(data[0] == 3):
					print("Se recibieron los datos que pedi correctamente")
					socket_pedir.close()
					break
					
			except:
				time.sleep(1)
				pass		
	
def getMAC():
	return uuid.getnode() 	

def registerNodeBC():
	global IP_Nodo
	sock_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_broadcast.setblocking(0)
	server_address = ('', PUERTO_BC)
	sock_broadcast.bind(server_address)

	while IP_Nodo == 0:
		try:
			data, address = sock_broadcast.recvfrom(BUFFER_SIZE)
			if(data != 0):
				data = struct.unpack(formatoBcast, data)
				
				IP_Nodo = address[0]	
				print('Soy ID le di pelota')
				
				if data[0] == 5: #aqui hay que chequear que el opcode del paquete haya sido el esperado, si no reenviar
					print ("Respondiendo por TCP....")
					respuestaTCP(IP_Nodo)
					break			
		except:
			print ("Esperando")
			time.sleep(2)
			pass
	print ("Register BC thread terminating")	
	
	# OpCodes Champions:
	#		0 -> Quiero ser
	#		1 -> Soy activa
	#		2 -> KeepAlive
def enviarQuieroSer():
	global ronda_champions, soy_activa, my_mac
	sock_quiero = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_quiero.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock_quiero.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	sock_quiero.settimeout(3) # timeout un thread que lo mate, este timeout es cuando tiempo esta escuchando


	my_mac = getMAC()
	server_address = ('255.255.255.255', PUERTO_CHAMPIONS)

	paquete_bcast = struct.pack('=BIB',quiero_ser_activa, my_mac,ronda_champions)
	try:
		print('Enviar quiero ser Activa')
		sent = sock.sendto(paquete_bcast, server_address)
		data, address = sock_quiero.recvfrom(BUFFER_SIZE)
		data_bcast = sock.unpack(formato_champions, data)
		que_quiere = data_bcast[0] 
		mac_contrincante = data_bcast[1] 
		
		if(my_mac != mac_contrincante):
			peleitas(que_quiere, mac_contrincante, my_mac)
				
	finally:	
		sock.close()
		print("Termino Bcast")
	return 0

def peleitas(que_quiere, mac_contrincante, my_mac):
	quiero_ser_activa = 0
	soy_activa = 1
	keep_alive = 2
	
	if (que_quiere ==  quiero_ser_activa):
		if(my_mac > mac_contrincante):
			
	elif( que_quiere == soy_activa):
		pass
	else: # que_quiere = keep_alive:
		pass
	
def enviarSoyActivo():
	global ronda_champions
	return 0
def responderQuieroSer():	
	global ronda_champions
	return 0	

def actualizar_todo_datos(data):
	return 0
	
def actualizar_datos(data):
	return 0
def main():
		
	thread_bcast = threading.Thread(target = registerNodeBC)
	#thread_bcast.start()
	registerNodeBC()
	thread_champions = threading.Thread(target = enviarQuieroSer)
	
	paquete = crearPaquete(1)
	paquete1 = crearPaquete(2)
	paquete2 = crearPaquete(3)
	
	sendTCP(paquete, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete1, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete2, IP_Nodo)	
	time.sleep(2)	

	print ("Pidiendo datos")
	
	paquetePedir = crearPaquetePedir()
	pedirTCP(paquetePedir, IP_Nodo)


	print ("MAC", getMAC())
	
main()
	
