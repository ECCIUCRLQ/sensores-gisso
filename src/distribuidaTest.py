import struct
import random
import socket
import time
import sys

MY_IP = '10.1.138.103'  # Mi IP
IP_Nodo = ''

formatoBcast = '=BI'
PUERTO_BC = 6000
PORT_NM = 3114

def crearPaquete(ID):
	datos = bytearray([0,2,3,4,5])
	formatoGuardar = "=BBI"
	tamPag = int(len(datos))
	print (tamPag)
	packGuardar = struct.pack(formatoGuardar,0,ID,tamPag)
	packGuardar += datos
	
	print (packGuardar)
	return packGuardar

def crearPaquete2():
	formatoGuardar = "=BB"
	packpedir = struct.pack(formatoGuardar,1,1)
	return packpedir
	
	

def respuestaTCP(IP_Nodo):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		print ("Enviando a", IP_Nodo )
		
		socket_send.connect((IP_Nodo, PORT_NM))
		paqueteRespuesta = struct.pack('=B',2)
		print ("Paquete:", paqueteRespuesta)
		socket_send.sendall(paqueteRespuesta)
		socket_send.close()
		print ("Respondi por TCP")

def sendTCP(paquete, IP_Nodo):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		while True:
			try:
				print ("Enviando paquete TCP",IP_Nodo)
				print ("Enviando paquete TCP 1",paquete)
				socket_send.connect((IP_Nodo, PORT_NM))
				print ("Holis")
				socket_send.sendall(paquete)
				print ("Holis2")
				data, address = socket_send.recvfrom(4096)
				print ("Holis3", data[0])
				print ("Dataaaaaaaaaaaaaaa", data)
				if(data[0] == 2):
					print("recibido correctamente")
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
				data, address = socket_pedir.recvfrom(4096)
				print ("Data", data)
				if(data[0] == 3):
					print("recibido pedir correctamente")
					socket_pedir.close()
					break
					
			except:
				time.sleep(1)
				pass		
	
	

def getNodeIP():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setblocking(0)
	server_address = ('', PUERTO_BC)
	sock.bind(server_address)

	while True:
		try:
			data, address = sock.recvfrom(4096)
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
	#sock.close()
	return IP_Nodo		
def main():	

	IP_Nodo = getNodeIP()
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
	
	paquetePedir = crearPaquete2()
	pedirTCP(paquetePedir, IP_Nodo)
	
main()
	
