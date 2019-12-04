import struct
import socket

IP_Nodo = '127.0.0.1'
IP_ID = '127.0.0.1'
PUERTO_ID = 3114

#Se crea socket para la comunicacion entre Memoria distribuida y nodo memoria (UDP)
def envioPackBC ():
	global IP_ID
	PORT_BC = 5000
	socketNodos = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Abrir los sockets
	#Crear paquete BC
	packRpta = struct.pack('BI', 5, 80000000)
	socketNodos.sendto(packRpta, (IP_ID, PORT_BC)) # Crea la conexion

#Prueba
envioPackBC()

socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_send.bind((IP_Nodo, PUERTO_ID))
socket_send.listen()
conn, addr = socket_send.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(4096)
        if not data:
            break
        pack = struct.pack('BBI', 2, data[1], 80000000)
        conn.sendall(pack)


while(True):
	data, addr = socket_send.recvfrom(50) # buffer size
	print ("Ya guarde")
	print(data)