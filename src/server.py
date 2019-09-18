import socket
import struct 
import time

MINE = "10.1.137.9"

UDP_PORT = 5000
FORMAT = 'BIBBBBBf'
ListaIdGrupo=["Whitenoise","FlamingoBlack","GISSO","KOF","Equipo 404","Poffis"]
listaSensores=["KeepAlive","Movimiento","Sonido","Luz","Shock","Touch","Humedad","BigSound","Temperatura","Ultrasonico"]

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((MINE, UDP_PORT))

archivo = open("datos.txt","w")

while True:
	data, addr = sock.recvfrom(50) # buffer size is 1024 bytes
	var = struct.unpack(FORMAT,data)
	t = var[1]
	t = time.ctime(t)
	packAck=struct.pack('BBBBB',var[0],var[2],0,0, var[5]) 
	sock.sendto(packAck, (addr))

	aEscribir = "Mensaje recibido de: " + ListaIdGrupo[var[2]-1] +"\n"+"Sensor: "+listaSensores[var[6]]+"\n"+"Numero Ack: "+str(var[0])+"\n"+"Fecha: " +str(t)+"\n"+"Dato: " +str(var[7])+"\n-------------------\n"
	
	print(aEscribir)	
	archivo.write(aEscribir)
	
archivo.close()	
