import socket
import struct 
import time

MINE = "10.1.137.9"

UDP_PORT = 10001
FORMAT = 'BiBBBBBf'
ListaIdGrupo=["Whitenoise","FlamingoBlack","GISSO","KOF","Equipo 404","Poffis"]
listaSensores=["KeepAlive","Movimiento","Sonido","Luz","Shock","Touch","Humedad","BigSound","Temperatura","Ultrasonico"]

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((MINE, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	var = struct.unpack(FORMAT,data)
	t = var[1]
	t = time.ctime(t)
	packAck=struct.pack('BBBBB',var[0],var[2],0,0, var[5]) 
	sock.sendto(packAck, (addr))
	print ("received message from group:", ListaIdGrupo[var[2]-1], " sensor: ", listaSensores[var[5]], " with: ", var[0], t, var[2], var[3], var[4] )
