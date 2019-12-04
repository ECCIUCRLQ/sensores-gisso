import struct
import random
import socket
import threading
import signal
import time
import sys
import uuid 

# Variables Globales
tablaNodos = [] 			# Columnas: NumeroNodo | IP | EspacioDisponible
tamanoTablaNodos = 0 		# Tamano de la tabla de nodos
tablaPaginas = [] 			# Columnas: NumeroPagina | NumeroNodo
tamanoTablaPaginas = 0 		# Tamano de la tabla de paginas
numeroNodo = 0 				# Identificador unico para cada nodo
killHilos = False
quieren_pelea = -1
mi_mac = -1
ronda_champions = 0
soy_activa = False
hay_activa = False
huboCambio = 0
# IPs
RED_LAB = '127.0.0.1'
IPActiva = '127.0.0.1'
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
IP_ML = ''
# Cromas
PORT_NM_ID = 6000
PORT_ID_ML = 2000
PORT_ID_NM = 3114
PORT_ID_ID = 6666
BUFFER_SIZE = 692000

# Formatos
formatoBcast = '=BI'

#Metodo para interrupcion
def keyboardInterruptHandler(signal, frame):
	global killHilos
	killHilos = True
	exit(0)
	signal.signal(signal.SIGINT, keyboardInterruptHandler)

def paqueteTCP_ML(idPagina):
	formatoRespuestaA = "=BB"
	paquete_respuesta = struct.pack(formatoRespuestaA,2,idPagina)
	
	return paquete_respuesta	

#Metodo para la comunicacion entre Memoria distribuida y los nodos de memoria (TCP)
def sendTCPNodo(paquete, IP_Nodo):
	global PORT_ID_NM
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		packRetorno = 0
		while True:
			try:
				socket_send.connect((IP_Nodo, PORT_ID_NM))
				socket_send.sendall(paquete)
				data,_ = socket_send.recvfrom(BUFFER_SIZE)
				if(data != 0):
					packRetorno = data
					socket_send.close()
					break

			except:
				print(threading.current_thread().name," Error al enviar: sendTCPNodo")
				pass
		print("TCP: ",packRetorno)		
	return packRetorno

#Metodo para la respuesta
def sendRptaBC(paquete, IP_Nodo):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		packRetorno = 0
		while True:
			try:
				socket_send.connect((IP_Nodo, PORT_ID_NM))
				socket_send.sendall(paquete)
				socket_send.close()
				break
			except:
				print(threading.current_thread().name," Error respondiendo: sendRptaBC")
				pass
	return packRetorno

def buscarIP(ipNodo):
	global tablaNodos,tamanoTablaNodos
	tengo = False
	index = 0

	while(index < tamanoTablaNodos):
		if(tablaNodos[index][1] == ipNodo):
			tengo = True
		index+=1	
	
	return tengo

def agregarNodoTabla(ipNodo, espacioNodo):
	global numeroNodo,tablaNodos,tamanoTablaNodos
	
	if not ( buscarIP(ipNodo) ):
		tablaNodos.append([])
		tablaNodos[tamanoTablaNodos].append(numeroNodo)
	
		tablaNodos[tamanoTablaNodos].append(ipNodo)
		tablaNodos[tamanoTablaNodos].append(espacioNodo)
	
		print(threading.current_thread().name," Se agregó en la tabla",tablaNodos)
		numeroNodo += 1
		tamanoTablaNodos += 1
	else:	
		print(threading.current_thread().name," Ya está en la tabla: agregarNodoTabla")
		
def elegirNodo(tamPaginaAGuardar):
	global tablaNodos,tamanoTablaNodos
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
	global tamanoTablaNodos, tablaNodos
	encontreNodo = False
	indiceNodo = -1
	i = 0
	while(i < tamanoTablaNodos and encontreNodo == False):
		if(tablaNodos[i][0] == numeroNodo):
			encontreNodo = True
			indiceNodo = i
		i += 1
	return indiceNodo

def actualizarDatos(indiceNodo, id_pagina, espacioDisponibleRecibido, numeroNodo):
	global tablaNodos, tablaPaginas, tamanoTablaPaginas

	tablaNodos[indiceNodo][2] = espacioDisponibleRecibido
	
	tablaPaginas.append([])
	tablaPaginas[tamanoTablaPaginas].append(id_pagina)
	tablaPaginas[tamanoTablaPaginas].append(numeroNodo)
	tamanoTablaPaginas+=1
	print(threading.current_thread().name," Tabla Paginas: ",tablaPaginas)
	
def mandarAGuardar(numeroNodo, packAGuardar):
	global PORT_ID_NM, tablaNodos
	
	id_pagina=0
	indiceNodo = 0
	ipNodo = 0
	#Se busca el nodo en la tabla de nodos para obtener su IP
	try:
		indiceNodo = buscaNodo(numeroNodo)
		if(indiceNodo != -1):
			ipNodo = tablaNodos[indiceNodo][1] #Necesaria para saber a quien se le envia el paquete.		
	except:
		print(threading.current_thread().name," Error buscando nodo")
	
	while True: # Enviar a guardar
		try:
			packRecibido = sendTCPNodo(packAGuardar, ipNodo) #Podria recibir 0
			datosPack = struct.unpack('=BBI',packRecibido)
			
			opCode = datosPack[0] #Si todo sale bien
			id_pagina = datosPack[1]
			espacioDisponibleRecibido = datosPack[2]
			print(threading.current_thread().name," Me retorno", datosPack,opCode)
			if( opCode == 2 ): #La condicion de este if puede cambiar a la vara del opCode (2), tambien se pude ver como el "Todo salio bien"
				print(threading.current_thread().name," Se guardo bien")
				actualizarDatos(indiceNodo,id_pagina, espacioDisponibleRecibido, numeroNodo)
				print(threading.current_thread().name," Paso actualizarDatos?")
				break
		except:
			print(threading.current_thread().name," Error al guardar: mandarAGuardar")	
			time.sleep(1)		
			pass
	
	print(threading.current_thread().name," Return guardado")
	return id_pagina

def guardar(packAGuardar):
	guardado = -1
	tamanoPagina = packAGuardar[1]
	while(guardado == -1):
		numeroNodo = elegirNodo(tamanoPagina)
		guardado = mandarAGuardar(numeroNodo, packAGuardar)
	return guardado	

#Busca la pagina y retorna el indice de la tabla de paginas en el que se encuentra
def buscaPagina(numeroPagina):
	global tablaPaginas,tamanoTablaPaginas
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
	global PORT_ID_NM, tablaNodos,tablaNodos
	#Se busca en la tabla de paginas la pagina solicitada
	indicePagina = buscaPagina(numeroPagina)
	nodo = tablaPaginas[indicePagina][1]
	#Se busca el nodo en la tabla de nodos para obtener su IP
	print("Antes buscar nodo")
	indiceNodo = buscaNodo(nodo)
	ipNodo = tablaNodos[indiceNodo][1] #Necesaria para saber a quien se le envia el paquete.
	#Para poder armar el paquete de pedir se necesitan los siguientes datos:
	opCode = 1
	idPagina = numeroPagina
	formatoEnvio = "=BB"
	packEnvio = struct.pack(formatoEnvio,opCode,idPagina)
	#Se envia el paquete a ipNodo mediante protocolo correspondiente y se recibe el paquete de respuesta
	print("Antes send TCPNodo")
	packRecibido = sendTCPNodo(packEnvio,ipNodo) #podria recibir 0
	print("Despues send TCPNodo")
	return packRecibido

def escucharML():
	global HOST,PORT_ID_ML,IP_ML
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketMLocal:
			socketMLocal.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			socketMLocal.bind(('127.0.0.1', PORT_ID_ML))
			socketMLocal.listen()
			conn, addr = socketMLocal.accept()##Movi esto 2 lineas mas arriba
			print("Conectado con: ",addr)
			with conn:
				while True:
					try:
						
						print("Esperando solicitud")
						packRec = conn.recv(BUFFER_SIZE) #Solo para que exista pero es el paquete recibido
						opCode = packRec[0]
						IP_ML = addr[0]
						if(opCode == 0): # Si se gurdó correctamente
							print("Guardando")
							id_pagina = guardar(packRec)
							paquete = paqueteTCP_ML(id_pagina)
							print(threading.current_thread().name," Paquete a ML: ",paquete, conn)
							conn.sendall(paquete)
							
						elif(opCode == 1): # Retorna si pedio
							print("Pidiendo")
							idPagina = packRec[1]
							paquete = pedirPagina(idPagina)
							conn.sendall(paquete)

					except:
						pass
			socketMLocal.close()
	
	# OpCodes Champions:
	#		0 -> Quiero ser
	#		1 -> Soy activa
	#		2 -> KeepAlive
	
def perdi_pelea():

	while True:
		pass
		# me quedo escuchando broadcast
		# break cuando muere keepalive
	
def recibir_dump(tabla):
	pass

def recibir_parte(data):
	pass

def champions():
	global quieren_pelea, mi_mac, ronda_champions, soy_activa, hay_activa
	mi_mac = getMAC().to_bytes(6,'little')

	socket_champions = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socket_champions.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	server_address = (RED_LAB, PORT_ID_ID)
	formatoBcast = '=B6sB'
	socket_champions.bind(server_address)
	while True:
		if not(hay_activa):
			paquete_bcast = struct.pack(formatoBcast,0, mi_mac,ronda_champions)
			socket_champions.sendto(paquete_bcast, server_address)
			data, _ = socket_champions.recvfrom(BUFFER_SIZE)

			if(data != 0):
				data = struct.unpack(formatoBcast, data)
				
				if(data[0] == 1):
					hay_activa = True
					recibir_dump(data)

				elif(data[0] == 0): # OpCode es yo quiero
					if(data[2] == ronda_champions): # Comparo ronda
						if( mi_mac > data[1]):
							ronda_champions+=1
						else:	
							soy_activa = False
		else:
			if not(soy_activa):
				data, _ = socket_champions.recvfrom(BUFFER_SIZE)
				if(data[0] == 2):
					pass


	socket_champions.close()

def accionHiloPrincipal():
	while(True):
		escucharML()

def accionHiloNodos():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setblocking(0)
	server_address = (RED_LAB, PORT_NM_ID)
	sock.bind(server_address)

	while True:
		try:
			data, address = sock.recvfrom(BUFFER_SIZE)
			if(data != 0):
				data = struct.unpack(formatoBcast, data)

				IP_Nodo = address[0]
				espacioDisponible = data[1]

				if data[0] == 5: #aqui hay que chequear que el opcode del paquete haya sido el esperado, si no reenviar
					print (threading.current_thread().name," Respondiendo por TCP....")
					agregarNodoTabla(IP_Nodo,espacioDisponible)

					paquete_respuesta = struct.pack('=B', 2)
					sendRptaBC(paquete_respuesta, IP_Nodo)
		except:
			print (threading.current_thread().name," Escuchando registros de nodos")
			time.sleep(2)
			pass
	sock.close()

def printNodos(tablaNodos, tamanoTablaNodos):
	index = 0
	print("\n============INPUT============")
	while(index < tamanoTablaNodos):
		print(tablaNodos[index])
		index+=1
	print("==============\n")
		
def printPaginas(tablaPaginas, tamanoTablaPaginas):	
	index = 0
	print("\n============INPUT============")
	while(index < tamanoTablaPaginas):
		print(tablaPaginas[index])
		index+=1
	print("==============\n")	

def getMAC():
	return uuid.getnode() 	

def responderComando():
	global tablaNodos, tablaPaginas, tamanoTablaPaginas, tamanoTablaNodos
	
	while True:
		commando = str(input())
		if(commando == "nodo"):
			printNodos(tablaNodos, tamanoTablaNodos)
		elif(commando == "pagina"):
			printPaginas(tablaPaginas, tamanoTablaPaginas)
		else:
			pass

def soyActiva():

	comunicacionIDs()

	hiloNodos = threading.Thread(target=accionHiloPrincipal,name='[Principal]') #Encargado de comunicar Local con Nodos y viceversa
	hiloNodos.start()
	
	hiloPrincipal = threading.Thread(target=accionHiloNodos,name="[Broadcast]") # Encargado de escuchar broadcasts de los nodos
	hiloPrincipal.start()

def crearDump():
	return 0

def crearPaqueteCambio():
	return 0

def comunicacionIDs():
	global huboCambio
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setblocking(0)
	server_address = (RED_LAB, PORT_ID_ID)
	sock.bind(server_address)

	while True:
		try:
			data, address = sock.recvfrom(BUFFER_SIZE)
			if(data[0] == 0):
				data = struct.unpack(formatoBcast, data)
				filas1 = struct.unpack("=B", data[1:2])[0]
				
				paqueteDump = crearDump()
				sock.sendto(paqueteDump, address)
		except:
			print (threading.current_thread().name," Escuchando IDS nuevas")

		if(huboCambio == 1):
			paqueteCambio = crearPaqueteCambio()
			sock.sendto(paqueteCambio, server_address)
			huboCambio = 0
		else:
			paqueteKeepAlive = struct.pack('=BB',2,0)
			sock.sendto(paqueteKeepAlive, server_address)
		time.sleep(2)	
	sock.close()

def iniciarHilos():
	global soyActiva

	#hiloInput = threading.Thread(target=responderComando,name="INPUT") # Hilo extra para debugeo
	#hiloInput.start()
	soyActiva()
	#accionHiloPrincipal()
	#hiloPelea = threading.Thread(target=champions,name='[Champions]') # encargado de 
	#hiloPelea.start()
	#while True:
	#	if(soyActiva):
	#		soyActiva()

iniciarHilos()



	
