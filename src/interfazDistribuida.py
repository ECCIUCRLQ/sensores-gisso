# coding: utf8

import struct
import random
import socket
import threading
import signal
import time
import sys
import uuid 
import os

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
soy_pasiva = False
hay_activa = False

activaViva = True
siLlego = False
huboCambio = 0
championsTimeOut = 0

contadorCambiosPagina = 0
cambiosPagina = []

contadorCambiosNodo = 0
cambiosNodo = []

# IPs
RED_LAB = '10.1.255.255'
IPActiva = '192.168.1.50'
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
IP_ML = ''

# Cromas
PORT_NM_ID = 8000
PORT_ID_ML = 2000
PORT_ID_NM = 3114
PORT_ID_ID = 6669
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
	global numeroNodo,tablaNodos,tamanoTablaNodos, cambiosNodo
	
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
	global tablaNodos, tablaPaginas, tamanoTablaPaginas, tablaPaginas

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
		
def recibir_dump(data):
	global tablaPaginas, tablaNodos, tamanoTablaPaginas, tamanoTablaNodos

	filaPaginasCambiadas = data[1]
	filasNodosCambiadas = data[2]
	dump1 = data[3]
	dump2 = data[4]
					
	for index in range(filaPaginasCambiadas):
		tablaPaginas.append([])
		for jindex in range(2):
			tablaNodos[tamanoTablaPaginas].append(dump1[index][jindex])			
		tamanoTablaPaginas+=1				

	for index in range(filasNodosCambiadas):
		tablaNodos.append([])
		for jindex in range(3):
			tablaNodos[tamanoTablaNodos].append(dump2[index][jindex])
		tamanoTablaNodos+=1


def chamTimeOut(segundos):
	global championsTimeOut

	print(threading.current_thread().name," Empieza Timeout")
	time.sleep(segundos)
	championsTimeOut = 1
	print(threading.current_thread().name," Fin Timeout")

def champions():
	global quieren_pelea, mi_mac, ronda_champions, soy_activa, hay_activa, championsTimeOut, soy_pasiva, huboCambio
	mi_mac = getMAC().to_bytes(6,'little')
	recibido = 0

	socket_champions = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socket_champions.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	socket_champions.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	socket_champions.setblocking(0)

	server_address = (RED_LAB, PORT_ID_ID)
	formato = '=B6sB'
	socket_champions.bind(server_address)
	hiloTimeOut = threading.Thread(target=chamTimeOut,args=(3,),name='[Timeout]') #Encargado de comunicar Local con Nodos y viceversa
	hiloTimeOut.start()

	mio = 0

	while championsTimeOut==0 and soy_pasiva == False:
		if not(soy_pasiva):
			if(mio == 0):
				paquete_bcast = struct.pack(formato,0, mi_mac,ronda_champions)
				_sent = socket_champions.sendto(paquete_bcast, server_address)
				print("Envio mensaje", _sent)

			while championsTimeOut==0 and recibido == 0:	
				try:
					
					data, _address = socket_champions.recvfrom(BUFFER_SIZE)
					print("Esperando datos",data)
					if( data != 0):	
						data = struct.unpack(formatoBcast, data)
						print(">>>Recibí mensajes", data)		
						if not(data[1] == mi_mac):
							print("Recibi alguien mas")
							
							if(data[0] == 1):
								recibido = 1
								print ("Primer if")
								soy_pasiva = True
								recibir_dump(data) # Falta implementar

							elif(data[0] == 0): # OpCode es yo quiero
								recibido = 1
								if(data[2] == ronda_champions): # Comparo ronda
									if( mi_mac > data[1]):
										ronda_champions+=1
									else:	
										print ("Segundo if")
										soy_pasiva = True
										ronda_champions = 3
								elif(data[2] > ronda_champions):
									print ("Tercer if")
									soy_pasiva = True
									ronda_champions = 3
						else:
							mio = 1	

				except:
					pass

				
			recibido = 0
		mio = 0
		
	championsTimeOut = 0
	if(soy_pasiva==True):
		pass
	else:
		paquete_bcast = struct.pack(formato,0, mi_mac,ronda_champions)
		socket_champions.sendto(paquete_bcast, server_address) ### Revisar esto
		hiloTimeOut = threading.Thread(target=chamTimeOut,args=(1,),name='[TimeOut]') 
		hiloTimeOut.start()
		while (championsTimeOut == 0 and recibido == 0 and soy_pasiva == True):
			try:
				data, _address = socket_champions.recvfrom(BUFFER_SIZE)
				
				if(data[0] == 0 and data[2]==ronda_champions): ##Revisar el paquete si es el que espero comparar Macs y revisar
					recibido = 1
					if(data[1] > mi_mac):
						soy_pasiva = True
					
			except:
				pass
	
	print ("despues del juail")
	
	if not(soy_pasiva):
		soy_activa = True
		dump1, dump2 = crearDump(huboCambio)
		paqueteCambio = paquete_broadcast_ID_ID(2,tamanoTablaPaginas,tamanoTablaNodos,dump1,dump2)
		socket_champions.sendto(paqueteCambio, server_address)


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
			time.sleep(1)
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
	print("MI MAC", uuid.getnode()  )
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

	hiloNodos = threading.Thread(target=accionHiloNodos,name="[Broadcast]") # Encargado de escuchar broadcasts de los nodos
	hiloNodos.start()

	hiloKA = threading.Thread(target=comunicacionIDs,name='[KeepAlive]') #Encargado de la comunicacion entre IDs
	hiloKA.start()

	hiloPrincipal = threading.Thread(target=accionHiloPrincipal,name='[Principal]') #Encargado de comunicar Local con Nodos y viceversa
	hiloPrincipal.start()
	
	

def paquete_broadcast_ID_ID(op_code, fila1, fila2, dump1, dump2):
	if (fila1 or fila2 > 0): # Hay Cambios
		formato = '=BBB'

		paquete = struct.pack(formato, op_code, fila1, fila2)
		paquete+=dump1
		paquete+=dump2

		return paquete
		
	else: # No hay cambios
		formato = '=BBB'
		
		paquete = struct.pack(formato, op_code, fila1,fila2)

		return paquete

def crearDump(huboCambio):
	global tamanoTablaNodos, tamanoTablaPaginas, tablaPaginas, tablaNodos
	global contadorCambiosNodo, contadorCambiosPagina, cambiosNodo, cambiosPagina

	dump1 = bytearray()
	dump2 = bytearray()

	for pagina in tablaPaginas:
		if huboCambio == 1: # con cambio
			for paginasCambiadas in cambiosPagina:
				if pagina == paginasCambiadas:
					dump1.append(pagina)
					dump1.append(tablaPaginas[pagina])
		else:
			dump1.append(pagina)
			dump1.append(tablaPaginas[pagina])

	for nodo in tablaNodos:
		if huboCambio == 1: #cambios
			for nodoCambio in cambiosNodo:
				if nodoCambio == nodo:
					dump2.append(nodo)
					data = tablaNodos[nodo]

					ipNodo = struct.pack("I", data[0])
					tamanoNodo = struct.pack("I", data[1])

					for i in range(4):
						dump2.append(ipNodo[i])

					for i in range(4):
						dump2.append(tamanoNodo[i])
		else:
			dump2.append(nodo)
			
			data = tablaNodos[nodo]

			ipNodo = struct.pack("I", data[0])
			tamanoNodo = struct.pack("I", data[1])

			for i in range(4):
				dump2.append(ipNodo[i])

			for i in range(4):
				dump2.append(tamanoNodo[i])	
	
	contadorCambiosNodo = contadorCambiosPagina = 0
	cambiosPagina = cambiosNodo = []

	return dump1, dump2	

def comunicacionIDs():
	global huboCambio, tamanoTablaPaginas, tamanoTablaNodos
	sock_comunicacion = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_comunicacion.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock_comunicacion.setblocking(0)

	server_address = (RED_LAB, PORT_ID_ID)
	sock_comunicacion.bind(server_address)

	while True:
		try:
			data, address = sock_comunicacion.recvfrom(BUFFER_SIZE)
			if(data[0] == 0): # Recibir yo quiero ser activa cuando soy activa
				data = struct.unpack(formatoBcast, data)
				dump1, dump2 = crearDump(0)
				paqueteDump = paquete_broadcast_ID_ID(1,tamanoTablaPaginas, tamanoTablaNodos, dump1, dump2)
				sock_comunicacion.sendto(paqueteDump, address)
		except:
			print (threading.current_thread().name," Escuchando IDs nuevas")

		if(huboCambio == 1):
			dump1, dump2 = crearDump(huboCambio)
			paqueteCambio = paquete_broadcast_ID_ID(2,contadorCambiosPagina,contadorCambiosNodo,dump1,dump2)
			sock_comunicacion.sendto(paqueteCambio, server_address)
			huboCambio = 0
			print (threading.current_thread().name," Actualizando datos")
		else:
			paqueteKeepAlive = paquete_broadcast_ID_ID(2,0,0,0,0)
			sock_comunicacion.sendto(paqueteKeepAlive, server_address)
			print (threading.current_thread().name," Estoy vivo")
		time.sleep(2)	
	sock_comunicacion.close()

def pasivaTimeout(segundos):
	global activaViva

	print(threading.current_thread().name," Empieza KA Timeout")
	time.sleep(segundos)
	if not(siLlego):
		activaViva = False
	print(threading.current_thread().name," Fin KA Timeout")

def soyPasiva():
	global tablaNodos, tablaPaginas, tamanoTablaNodos, tamanoTablaPaginas, activaViva, siLlego
	
	socket_pasiva = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socket_pasiva.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	socket_pasiva.setblocking(0)

	server_address = (RED_LAB, PORT_ID_ID)
	formatoBcast = '=B6sB'
	
	socket_pasiva.bind(server_address)
	
	hiloTimeout = threading.Thread(target=pasivaTimeout,args=(4,),name='[KA Timeout]')

	while activaViva:
		try:
			data, _ = socket_pasiva.recvfrom(BUFFER_SIZE)
			data = struct.unpack(formatoBcast, data)	
			
			if( data[0] == 2): # llego KeepAlive
				siLlego = True
				if( data[1] != 0 or data[2] != 0 ): # trae datos
					recibir_dump(data)

		except:
			if (siLlego):
				hiloTimeout.start() 
			siLlego = False
			time.sleep(2)
	

	socket_pasiva.close()
	iniciarInterfaz()

def iniciarInterfaz():
	global soy_activa

	champions()
	if(soy_activa):
		print ("[Principal]  Soy activa")
		#os.system('ifconfig eth0 down')
		#os.system('ifconfig eth0 ' + str(IPActiva))
		#os.system('ifconfig eth0 up')
		soyActiva()
	else:
		print ("[Principal]  Soy pasiva")
		soyPasiva()


iniciarInterfaz()