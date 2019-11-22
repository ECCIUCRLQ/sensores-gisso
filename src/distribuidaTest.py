import struct
import random
import socket
import time
import sys

MY_IP = '10.1.137.177'  # Mi IP
IP_Nodo = ''

def crearPaquete():
	datos = bytearray([0,2,3,4,5])

	formatoGuardar = "BBI" + str(len(datos)) +"s"
	formato = "BBIB"
	tamPag = len(datos)
	packGuardar = struct.pack(formatoGuardar,0,1,tamPag,datos)

	return packGuardar

def sendTCP(paquete, IP_Nodo):
	
	PORT_NM = 3114
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		print("holis1",IP_Nodo)
		
		while True:
			try:
				socket_send.connect((IP_Nodo, PORT_NM))
				print("holis2")
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
	server_address = ('', 5000)

	sock.bind(server_address)

	response = 'pfg_ip_response_serv'

	while True:
		try:
			data, address = sock.recvfrom(4096)
			if(data != 0):
				data = str(data.decode('UTF-8'))
				
				IP_Nodo = address[0]
				print(IP_Nodo)		
				
				if data == 'pfg_ip_broadcast_cl': #aqui hay que chequear que el opcode del paquete haya sido el esperado, si no reenviar
					print('Soy ID le di pelota')
					sent = sock.sendto(response.encode(), address)
				break		
		except:
			print ("Esperando")
			time.sleep(2)
			pass
	#sock.close()
	return IP_Nodo		
def main():	

	IP_Nodo = getNodeIP()
		
	print("IP_Nodo", IP_Nodo)	

	paquete = crearPaquete()
	
	sendTCP(paquete, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete, IP_Nodo)	
	time.sleep(2)
	sendTCP(paquete, IP_Nodo)	

main()
	
