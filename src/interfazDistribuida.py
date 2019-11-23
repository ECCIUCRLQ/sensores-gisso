import struct
import random
import socket
import threading 
import signal

tablaNodos = [] # Columnas: NumeroNodo | IP | EspacioDisponible
tamanoTablaNodos = 0 # Tamano de la tabla de nodos
tablaPaginas = [] # Columnas: NumeroPagina | NumeroNodo
tamanoTablaPaginas = 0 # Tamano de la tabla de paginas
numeroNodo = 0 # Identificador unico para cada nodo

#Se crea socket para la comunicacion entre Memoria local e Interfaz distribuida (TCP)
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 2000        # Port to listen on (non-privileged ports are > 1023)
socketMLocal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketMLocal.bind((HOST, PORT))
socketMLocal.listen()
conn, addr = socketMLocal.accept() 

puertoNodos = 3114

#Se crea socket para la comunicacion entre Memoria distribuida y nodo memoria mediante broadcast (UDP)
IPActiva = '127.0.0.1'
PORT_BC_NM = 5000
socketNodos = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Abrir los sockets
socketNodos.bind((IPActiva, PORT_BC_NM))	# Crea la conexion 

#Bool para poder matar a los hilos secundarios
killHilos = False

#Metodo para interrupcion
def keyboardInterruptHandler(signal, frame):
	global killHilos
	killHilos = True
	exit(0)
signal.signal(signal.SIGINT, keyboardInterruptHandler)

#Metodo para la comunicacion entre Memoria distribuida y los nodos de memoria (TCP)
def sendTCPNodo(paquete, IP_Nodo):
	global puertoNodos
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		packRetorno = 0
		while True:
			try:
				socket_send.connect((IP_Nodo, puertoNodos))
				socket_send.sendall(paquete)
				data = socket_send.recvfrom(4096)
				if(data != 0):
					packRetorno = data
					socket_send.close()
					break
				
			except:
				pass	
	return packRetorno

#Metodo para la respuesta
def sendRptaBC(paquete, IP_Nodo):
	global puertoNodos
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		packRetorno = 0
		while True:
			try:
				socket_send.connect((IP_Nodo, puertoNodos))
				socket_send.sendall(paquete)
				socket_send.close()
				break
				
			except:
				pass	
	return packRetorno

def agregarNodoTabla(ipNodo, espacioNodo):
	global numeroNodo
	tablaNodos[tamanoTablaNodos].append(numeroNodo)
	numeroNodo += 1
	tablaNodos[tamanoTablaNodos].append(ipNodo)
	tablaNodos[tamanoTablaNodos].append(espacioNodo)
	tamanoTablaNodos += 1

def elegirNodo(tamPaginaAGuardar):
	nodoElecto = False
	numNodoElegido = -1
	i = 0
	while(i < tamanoTablaNodos and nodoElecto == False):
		if(tablaNodos[i][2] >= tamPaginaAGuardar):
			nodoElecto = True
			numNodoElegido = tablaNodos[i][0]
		i += 1
	return numNodoElegido

#Busca el nodo y retorna el indice de la tabla de nodos en el que se encuentra.
def buscaNodo (numeroNodo):
	encontreNodo = False
	indiceNodo = -1
	i = 0
	while(i < tamanoTablaNodos and encontreNodo == False):
		if(tablaNodos[i][0] == numeroNodo):
			encontreNodo = True
			indiceNodo = i
		i += 1
	return indiceNodo

def mandarAGuardar(numeroNodo, packAGuardar):
	global puertoNodos, socketMLocal, socketNodos
	guardado = False #Booleano para saber si se guardo correctamente
	#Se busca el nodo en la tabla de nodos para obtener su IP
	indiceNodo = buscaNodo(numeroNodo)
	ipNodo = tablaNodos[indiceNodo][1] #Necesaria para saber a quien se le envia el paquete.
	#Se envia el paquete a esa IP mediante el respectivo protocolo TCP y se recibe la respuesta
	packRecibido = sendTCPNodo(packGuardar, ipNodo) #Podria recibir 0
	datosPack = struct.unpack('BBI',packRecibido)
	opCode = datosPack[0]
	#Si todo sale bien 
	if( opCode == 2 ): #La condicion de este if puede cambiar a la vara del opCode (2), tambien se pude ver como el "Todo salio bien"
		espacioDisponibleRecibido = datosPack[2] 
		idPagina = datosPack[1]
		#Actualizar el espacio disponible en la tabla de nodos
		tablaNodos[indiceNodo][2] = espacioDisponibleRecibido
		#Se agrega en la tabla de paginas
		tablaPaginas[tamanoTablaPaginas].append(idPagina)
		tablaPaginas[tamanoTablaPaginas].append(numeroNodo)
		guardado = True 
		#Enviar paquete de respuesta a Aministrador de Memoria
		formatoRespuestaA = "BB" 
		packRes = struct.pack(formatoRespuestaA,opCode,idPagina)
		socketMLocal.sendall(packRes)
	return guardado

def guardar(packAGuardar):
	guardado = False
	while(guardado == False):
		numeroNodo = elegirNodo(tamanoPagina)
		guardado = mandarAGuardar(numeroNodo, packAGuardar)

#Busca la pagina y retorna el indice de la tabla de paginas en el que se encuentra
def buscaPagina(numeroPagina):
	paginaEncontrada = False
	indicePagina = -1
	i = 0
	while(i < tamanoTablaPaginas and paginaEncontrada == False):
		if(tablaPaginas[i][0] == numeroPagina):
			paginaEncontrada = True
			indicePagina = i
		i += 1
	return indicePagina

#Se va a ver si se pasa tambien pack armado por parametro o se vuelve a armar dentro de metodo como se esta haciendo.
def pedirPagina(numeroPagina):
	global puertoNodos, socketMLocal, socketNodos
	#Se busca en la tabla de paginas la pagina solicitada
	indicePagina = buscaPagina(numeroPagina)
	nodo = tablaPaginas[indicePagina][1]
	#Se busca el nodo en la tabla de nodos para obtener su IP
	indiceNodo = buscaNodo(nodo)
	ipNodo = tablaNodos[indiceNodo][1] #Necesaria para saber a quien se le envia el paquete.
	#Para poder armar el paquete de pedir se necesitan los siguientes datos:
	opCode = 1
	idPagina = numeroPagina
	formatoEnvio = "BB" 
	packEnvio = struct.pack(formatoEnvio,opCode,idPagina)
	#Se envia el paquete a ipNodo mediante protocolo correspondiente y se recibe el paquete de respuesta
	packRecibido = sendTCPNodo(packEnvio,ipNodo) #podria recibir 0

	#Se envia por paquete el paquete recibido al administrador de memoria. (Sin importar su opCode)
	socketMLocal.sendall(packRecibido)


def accionHiloPrincipal():
	while(True):
		#Estoy escuchando mediante el receive
		#Recibo el pack packRec
		packRec = conn.recv(1024) #Solo para que exista pero es el paquete recibido 
		opCode = packRec[0]
		if(opCode == 0):
			guardar(packRec)
		elif(opCode == 1):
			idPagina = packRec[1]
			pedirPagina(idPagina)

def accionHiloNodos():
	global PORT_BC_NM, socketNodos, killHilos
	while(killHilos == False):
		data, addr = socketNodos.recvfrom(50) # buffer size
		datosPack = struct.unpack('BI', data)
		opCode = datosPack[0]

		if(opCode == 5):
			espacioDisponible = datosPack[1]
			ip = socket.inet_aton(addr)
			agregarNodoTabla(ip, espacioDisponible)
			#Creo paquete de respuesta
			packRpta = struct.pack('B', 2)
			sendRptaBC(packRpta, ip)

#Se crea el hilo que atiende a los nodos (Cuando quieren ser nodos)
hiloNodos = threading.Thread(target=accionHiloNodos)
hiloNodos.start()

#(Guardar y pedir)
accionHiloPrincipal()
