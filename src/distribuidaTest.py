import struct
import random
import socket
import time
import sys

MY_IP = '10.1.138.103'  # Mi IP
IP_Nodo = ''

formatoBcast = 'BI'
PUERTO_BC = 5000
PORT_NM = 3114

def crearPaquete():
	datos = bytearray([0,2,3,4,5])
	formatoGuardar = "=BBI"
	tamPag = int(len(datos))
	print (tamPag)
	packGuardar = struct.pack(formatoGuardar,0,1,tamPag)
	packGuardar += datos
	
	print (packGuardar)
	return packGuardar

def sendTCP(paquete, IP_Nodo):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		while True:
			try:
				socket_send.connect((IP_Nodo, PORT_NM))
				socket_send.sendall(paquete)
				data = socket_send.recvfrom(4096)
				if(data != 0):
					socket_send.close()
					break
					
			except:
				pass		
	

def getNodeIP():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setblocking(0)
	server_address = ('', PUERTO_BC)
	sock.bind(server_address)

	response = 'pfg_ip_response_serv'
	
	opCode = 2
	while True:
		try:
			data, address = sock.recvfrom(4096)
			if(data != 0):
				data = struct.unpack(formatoBcast, data)
				
				IP_Nodo = address[0]	
				
				if data[0] == 5: #aqui hay que chequear que el opcode del paquete haya sido el esperado, si no reenviar
					print('Soy ID le di pelota')
					paqueteRespuesta = struct.pack('B',opCode)
					sent = sock.sendto(paqueteRespuesta, address)
				break			
		except:
			print ("Esperando")
			time.sleep(2)
			pass
	#sock.close()
	return IP_Nodo		
def main():	

	IP_Nodo = getNodeIP()
	paquete = crearPaquete()
	
	sendTCP(paquete, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete, IP_Nodo)	

main()
	
