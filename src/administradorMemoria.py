# coding: utf8
import struct
import time
import random
from ipcqueue import sysvmq
import pdb
import socket
#IPDistribuida = 192.168.1.100
PORT = 2000           # Port to listen on (non-privileged ports are > 1023)
IPDistribuida = '10.1.137.17'
numeroPagina = 0
memoriaPrincipal = [] #Memoria principal o local
numeroFilasMemoria = 4
contadorFilaActual = 0
max8 = 10#10575
max5 = 10#16920
buzonLlamados = sysvmq.Queue(17)
buzonRetornos = sysvmq.Queue(16)
buzonParametros = sysvmq.Queue(15)


#Codigos de llamados
#HabilitarPagina = 0
#pedirPagina =1
#guardar=2

for i in range(numeroFilasMemoria):
    memoriaPrincipal.append([])


#Metodo para la comunicacion entre Memoria distribuida y los nodos de memoria (TCP)
def sendTCP(paquete):
	global PORT
	print("Hola entre------")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		packRetorno = 0
		while True:
			try:
				print("Antes del connect")
				socket_send.connect((IPDistribuida, PORT))
				socket_send.sendall(paquete)
				print ("Despues del connect")
				data = socket_send.recvfrom(4096)
				print("Recibido ", data)
				if(data != 0):
					packRetorno = data
					socket_send.close()
					break
				
			except:
				pass	
	return packRetorno

def pasarPaginaLocalADistribuida(indPagSwap): #Recibe el indice de la página a hacer swap y pasa una página (arreglo) a memoria distribuida por medio de un paquete mediante un socket.
	global memoriaPrincipal, s
	
	guardado = False #Para ver si la pagina se pudo guardar correctamente en memoria distribuida
	
	#Para el paquete de mandar a guardar en M.Distribuida se ocupan los siguientes datos:
	opCode = 0
	idPagina = memoriaPrincipal[indPagSwap][0]
	tamPag = 0 #Tamano de la pagina a la que se le esta haciendo swap en ese momento.
	if( memoriaPrincipal[indPagSwap][1] == 5 ):
		tamPag = len(memoriaPrincipal[indPagSwap]) * 5 #Para tener el tamano en bytes 
	elif( memoriaPrincipal[indPagSwap][1] == 8 ):
		tamPag = len(memoriaPrincipal[indPagSwap]) * 8 #Tamano en bytes
	datosPag = memoriaPrincipal[indPagSwap][:]
	print("Datos Pagina:", type(datosPag))
	print (datosPag)
	tamPag = int(len(datosPag))
	formatoGuardar = "=BBI"
	#Se empaquetan
	packGuardar = struct.pack(formatoGuardar,opCode,idPagina,tamPag)
	print ("PackGuardar: ",tamPag, packGuardar)
	packGuardar += b''.join(datosPag[2:])
	print ("Paquete A guardar",packGuardar)
	#Se envian esos datos mediante el protocolo TCP
	#s.sendall(packGuardar)
	
	packRecibido = sendTCP(packGuardar)

	#Para borrar la pagina de memoria local
	del memoriaPrincipal[indPagSwap][:]
	
	#Se recibe una confirmacion con: 
	packRecibido = s.recv(1024)
	datosPack = struct.unpack('BB',packRecibido)
	opCode = datosPack[0]
	opCode = packRecibido[0]
	#Si no hubo error
	if(opCode == 2):
		guardado = True
	#idPagina
	print("Salio Guardado")
	return guardado

def pasarPaginaDistribuidaALocal(indPagSwap, numP):
	global memoriaPrincipal

	recibido = False #Para ver si la pagina solicitada a memoria distribuida se recibio correctamente.

	#Para el paquete de pedir a la interfaz distribuida una pagina se ocupan los siguientes datos:
	opCode = 1
	idPagina = numP
	#Se empaquetan y se envian los datos mediante el protocolo correspondiente.
	formatoPedir = "=BB"
	packPedir = struct.pack(formatoPedir,opCode,idPagina)
	s.sendall(packPedir)
	packRecibido = sendTCP(packPedir)
	#Se recibe el paquete de respuesta
	formatoConfirmacion = "BB"+ str(len(packRecibido)-2)+"s"
	formatoConfirmacion = "=BB"
	tamanoPack = int(len(packRecibido)-2)
	datosPack = struct.unpack(formatoConfirmacion,packRecibido)
	opCodeR = datosPack[0]
	opCodeR = packRecibido[0]
	#En caso de que no haya error:
	#Se recibe la pagina solicitada	
	datosPagina = packRecibido[2:len(packRecibido)]
	#Colocar la pagina en memoria local
	memoriaPrincipal[indPagSwap] = datosPagina[:]

	#Si no hubo error 
	if(opCodeR == 3):
		recibido = True
	return recibido
	
def busquedaPaginaSwap(): #Sirve para localizar el indice de la pagina en la que se va a ser swap.
	global memoriaPrincipal, max5, max8, numeroFilasMemoria
	pagSwapB = False
	indMemSwap = -1
	#Se recorre la memoria principal buscando una llena
	i = 0
	while(i<numeroFilasMemoria and pagSwapB == False):
		if( paginallenaMemoriaPrincipal(i) == True ):
			pagSwapB = True 
			indMemSwap = i
		i += 1

	#Si ninguna esta llena.
	if(pagSwapB == False):
		#Escoje una random
		indMemSwap = random.randint(0,numeroFilasMemoria-1)
	return indMemSwap


def busquedaPaginaMemoriaPrincipal(numPABuscar):#Sirve para localizar el indice de la pagina que se esta buscando en memPrincipal
	global memoriaPrincipal
	indiceARetornar = -1
	paginaEncontrada = False
	i = 0
	while(i<numeroFilasMemoria and paginaEncontrada==False):
		if(len(memoriaPrincipal[i]) > 0 and memoriaPrincipal[i][0]==numPABuscar):
			indiceARetornar = i
			paginaEncontrada = True
		i += 1
	return indiceARetornar
			
			
#Habilitarle una pagina a un proceso y la coloca en la memoria principal     
def habilitarPagina(tamanoCelda):
	global numeroPagina, contadorFilaActual,memoriaPrincipal,max5,max8,numeroFilasMemoria
	#Para cuando la memoria principal tiene filas vacias
	if (contadorFilaActual < numeroFilasMemoria): 
		memoriaPrincipal[contadorFilaActual].append(numeroPagina)
		numeroPagina += 1
		memoriaPrincipal[contadorFilaActual].append(tamanoCelda)
		contadorFilaActual += 1
		
	#Cuando esta llena, entonces se empieza a hacer swap.
	else:
		indMemSwap = busquedaPaginaSwap()
		guardado = False
		while (guardado == False):
			guardado = pasarPaginaLocalADistribuida(indMemSwap)
		#Agregar nueva pagina en memoria local
		memoriaPrincipal[indMemSwap].append(numeroPagina)
		numeroPagina += 1
		memoriaPrincipal[indMemSwap].append(tamanoCelda)
	return numeroPagina-1


#Es para entregarle a la interfaz la pagina solicitada.		
def pedirPagina(numeroP):
	global memoriaPrincipal,numeroFilas,max5,max8
	paginaADevolver = []	
	indicePaginaADevolver = busquedaPaginaMemoriaPrincipal(numeroP)
	#Esta en memoria
	if (indicePaginaADevolver != -1):
		paginaADevolver = memoriaPrincipal[indicePaginaADevolver][:]
	#No esta en memoria
	else:
		#Hace swap
		indMemSwap = busquedaPaginaSwap()
		guardado = False
		while (guardado == False):
			guardado = pasarPaginaLocalADistribuida(indMemSwap)
		recibido = False
		while (recibido == False):
			recibido = 	pasarPaginaDistribuidaALocal(indMemSwap,numeroP)
		#Se toma de la memoria local la pagina deseada
		paginaADevolver = memoriaPrincipal[indMemSwap][:]
		
	return paginaADevolver
	
def paginallenaMemoriaPrincipal(indiceP): #Verificar por medio de un indice si una pagina esta llena en memoria local
	paginaLlena = False
	if(len(memoriaPrincipal[indiceP]) != 0 and memoriaPrincipal[indiceP][1] == 5):
		if(len(memoriaPrincipal[indiceP]) == max5):
			paginaLlena = True
	elif(len(memoriaPrincipal[indiceP]) != 0 and memoriaPrincipal[indiceP][1] == 8):
		if(len(memoriaPrincipal[indiceP]) == max8):
			paginaLlena = True
	return paginaLlena
	
def guardar(pack,numP): #Guarda en memoria. Puede tener varias condiciones que la pagina(que le da la intefaz local) este en memoria principal pero no este llena entonces solo guarda
						#Que este en memoria principal pero la pagina esta llena y que la pagina no este en memoria principal
	global numeroFilas, memoriaPrincipal,max5,max8
	print("NumeroPagina pos 0 memoria " + str (memoriaPrincipal))
	numeroPag = -1 #Se retorna a la interfaz, para saber si se le habilito una nueva pagina a ese sensor o no(-1).
	indiceP = busquedaPaginaMemoriaPrincipal(numP)
	#print(indiceP)
	#Si esta en memoria principal
	if(indiceP != -1):
		#print("Se llama a paginaLlena con indice" + str(indiceP))
		#Reviso si la pagina esta llena.
		paginaLlena = paginallenaMemoriaPrincipal(indiceP)
		#Si tiene espacio
		#print ("Pagina llena de guardar " + str(paginaLlena))
		if(paginaLlena == False):
			#Guarda el dato
			memoriaPrincipal[indiceP].append(pack)
		#Si esta llena
		else:
			#print ("Esta entrando al else que dice que esta llena")
			#Se habilita una nueva pagina
			pagNueva = habilitarPagina(memoriaPrincipal[indiceP][1])
			#Ver en que posicion de memoria local quedo, y luego ya se puede guardar
			indiceP = busquedaPaginaMemoriaPrincipal(pagNueva)
			#Se guarda
			memoriaPrincipal[indiceP].append(pack)
			numeroPag = pagNueva
	#Si no esta en memoria local 
	else:
		#print("Entre al else")
		indMemSwap = busquedaPaginaSwap()
		
		#print("Indice swap:" + str(indMemSwap))
		guardado = False
		while (guardado == False):
			guardado = pasarPaginaLocalADistribuida(indMemSwap)
		recibido = False
		while (recibido == False):
			recibido = pasarPaginaDistribuidaALocal(indMemSwap,numP)
		paginaLlena = paginallenaMemoriaPrincipal(indMemSwap) #(Revisar)
		#Si tiene espacio 
		if(paginaLlena == False):
			#Se guarda
			memoriaPrincipal[indMemSwap].append(pack)
		#Si esta llena
		else:
			#print ("Esta entrando al otro else en donde se dice que la pagina esta llena")
			pagNueva = habilitarPagina(memoriaPrincipal[indMemSwap][1])
			indMemSwap = busquedaPaginaMemoriaPrincipal(pagNueva)
			memoriaPrincipal[indMemSwap].append(pack)
			numeroPag = pagNueva
	return numeroPag
	
while(True):
	codigoLlamado = buzonLlamados.get()
	#print(codigoLlamado)
	if(codigoLlamado == 0): #Llama a Habilitar pagina
		parametro = buzonParametros.get() #Saco parametros
		paginaHabilitada = habilitarPagina(parametro)
		buzonRetornos.put(paginaHabilitada) #Envio lo que me retorno la funcion
		#print ("Realizo metodo habilitarPagina")
	elif(codigoLlamado == 1):#Llama a pedir pagina
		parametro = buzonParametros.get()
		paginaADevolver = pedirPagina(parametro)
		#print("BUZON RETORNO: ",paginaADevolver)
		buzonRetornos.put(paginaADevolver)
		
	elif(codigoLlamado == 2): #Llama a guardar 
		parametro1 = buzonParametros.get()
		parametro2 = buzonParametros.get()
		numPage = guardar(parametro1,parametro2)
		buzonRetornos.put(numPage)
		#print ("Realizo el metodo guardar")
	
		
			

	
			
			
			
			
		
	

