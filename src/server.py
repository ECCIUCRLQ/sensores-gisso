import socket
import struct 
import time

MINE = "10.1.137.9"

UDP_PORT = 10001
FORMAT = 'BIBBBBBf'
ListaIdGrupo=["Whitenoise","FlamingoBlack","GISSO","KOF","Equipo 404","Poffis"]
listaSensores=["KeepAlive","Movimiento","Sonido","Luz","Shock","Touch","Humedad","BigSound","Temperatura","Ultrasonico"]

sock = socket.socket(socket.AF_INET, # Creacion del socket
                     socket.SOCK_DGRAM) 
sock.bind((MINE, UDP_PORT))# Se establece la conexion

archivo = open("datos.txt","w") # Se abre el archivo a escribir los datos que recibio

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

	aEscribir = "Mensaje recibido de: " + ListaIdGrupo[var[2]-1] +"\n"+"Sensor: "+listaSensores[var[6]]+"\n"+"Numero Ack: "+str(var[0])+"\n"+"Fecha: " +str(t)+"\n"+"Dato: " +str(var[7])+"\n-------------------\n"
	print(aEscribir)	
	archivo.write(aEscribir) # Escribimos en archivo
	
archivo.close()	
