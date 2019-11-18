import struct
import random
import socket
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 2000        # Port to listen on (non-privileged ports are > 1023)
tablaNodos = [] # Columnas: NumeroNodo | IP | EspacioDisponible
tamanoTablaNodos = 0 #Tamano de la tabla de nodos
tablaPaginas = [] # Columnas: NumeroPagina | NumeroNodo
tamanoTablaPaginas = 0 #Tamano de la tabla de paginas
numeroNodo = 0 #Identificador unico para cada nodo
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

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
	guardado = False #Booleano para saber si se guardo correctamente
	#Se busca el nodo en la tabla de nodos para obtener su IP
	indiceNodo = buscaNodo(numeroNodo)
	ipNodo = tablaNodos[indiceNodo][1] #Necesaria para saber a quien se le envia el paquete.
	#Se envia el paquete a esa IP mediante el respectivo protocolo.

	#Se recibe la respuesta
	
	#Si todo sale bien 
	if( opCode == 2 ): #La condicion de este if puede cambiar a la vara del opCode (2), tambien se pude ver como el "Todo salio bien"
		espacioDisponibleRecibido = 0 #Va a ser lo que se recibe en el paquete de respuesta en vez de ese 0.
		#Actualizar el espacio disponible en la tabla de nodos
		tablaNodos[indiceNodo][2] = espacioDisponibleRecibido
		#Se agrega en la tabla de paginas
		tablaPaginas[tamanoTablaPaginas].append(idPagina)
		tablaPaginas[tamanoTablaPaginas].append(numeroNodo)
		guardado = True 
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
	recibido = False #Para ver si la pagina solicitada al nodo se recibio correctamente.
	#Se busca en la tabla de paginas la pagina solicitada
	indicePagina = buscaPagina(numeroPagina)
	nodo = tablaPaginas[indicePagina][1]
	#Se busca el nodo en la tabla de nodos para obtener su IP
	indiceNodo = buscaNodo(nodo)
	ipNodo = tablaNodos[indiceNodo][1] #Necesaria para saber a quien se le envia el paquete.
	#Para poder armar el paquete de pedir se necesitan los siguientes datos:
	opCode = 1
	idPagina = numeroPagina
	#Se envia el paquete a ipNodo mediante protocolo correspondiente
	
	#Se recibe el paquete de respuesta
	#opCode = a el opCode recibido en el paquete
	datosRecibidos = 0 #El 0 se debe cambiar por los datos que recibo en el paquete de respuesta 
	
	#Se envia por paquete el paquete recibido al administrador de memoria. (Sin importar su opCode)

"""
while(True):
	#Estoy escuchando mediante el receive
	#Recibo el pack packRec
	packRec = 0 #Solo para que exista pero es el paquete recibido
	#Se desarma el paquete en packRec en datosPack
	datosPack = 0 # Se sustituye el cero por el paquete recibido 
	opCode = datosPack[0]
	if(opCode == 0):
		guardar(packRec)
	elif(opCode == 1):
		idPagina = datosPack[1]
		pedirPagina(idPagina)
"""
