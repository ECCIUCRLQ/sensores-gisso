# coding: utf8
import struct
import time
import random
from ipcqueue import sysvmq
import pdb
import socket
#IPDistribuida = 192.168.1.100
PORT = 2000           # Port to listen on (non-privileged ports are > 1023)
IPDistribuida = '10.1.137.53'
numeroPagina = 0
tamanoPaginaTotal = 84600
memoriaPrincipal = [] #Memoria principal o local
#Hay que agregar frame table
pageArray = [] # Contiene los ID Pagina que estan en memoria Local
numeroFilasMemoria = 4 #Tamano de la memoria local
contadorFilaActual = 0
buzonLlamados = sysvmq.Queue(17)
buzonRetornos = sysvmq.Queue(16)
buzonParametros = sysvmq.Queue(15)
contadorPrueba = 0

#Codigos de llamados
#HabilitarPagina = 0
#pedirPagina =1
#guardar=2

for i in range(numeroFilasMemoria):
    memoriaPrincipal.append(bytearray([]))

#Se llena el pageArray
for i in range(numeroFilasMemoria):
	pageArray.append(-1) #El -1 indica que esta vacia 


#Metodo para la comunicacion entre Memoria distribuida y los nodos de memoria (TCP)
def sendTCP(paquete):
	global PORT, IPDistribuida
	print("Hola entre------")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_send:
		packRetorno = 0
		while True:
			try:
				print("Antes del connect")
				socket_send.connect((IPDistribuida, PORT))
				socket_send.sendall(paquete)
				print ("Despues del connect")
				data = socket_send.recv(4096)
				print("Recibido ", data)
				if(data != 2):
					packRetorno = data
					socket_send.close()
					break
				
			except:
				time.sleep(1)
				pass	
	return packRetorno

def pasarPaginaLocalADistribuida(indPagSwap): #Recibe el indice de la página a hacer swap y pasa una página (arreglo) a memoria distribuida por medio de un paquete mediante un socket.
	global memoriaPrincipal, tamanoPaginaTotal, pageArray
	
	guardado = False #Para ver si la pagina se pudo guardar correctamente en memoria distribuida
	
	#Para el paquete de mandar a guardar en M.Distribuida se ocupan los siguientes datos:
	opCode = 0
	#idPagina = memoriaPrincipal[indPagSwap][0]
	idPagina = pageArray[indPagSwap]
	tamPag = tamanoPaginaTotal
	datosPag = memoriaPrincipal[indPagSwap] # Copiar los datos de la pagina 
	formatoGuardar = "=BBI"
	#Se empaquetan
	packGuardar = struct.pack(formatoGuardar,opCode,idPagina,tamPag)
	#packGuardar += b''.join(datosPag[2:])
	packGuardar += datosPag
	#Se envian esos datos mediante el protocolo TCP
	packRecibido = sendTCP(packGuardar)

	#Para borrar la pagina de memoria local
	del memoriaPrincipal[indPagSwap]
	pageArray[indPagSwap] = -1
	
	#Se recibe una confirmacion con: 
	#datosPack = struct.unpack('BB',packRecibido)
	opCode = packRecibido[0]
	#Si no hubo error
	if(opCode == 2):
		guardado = True
	#idPagina
	return guardado

def pasarPaginaDistribuidaALocal(indPagSwap, numP):
	global memoriaPrincipal, tamanoPaginaTotal, pageArray

	recibido = False #Para ver si la pagina solicitada a memoria distribuida se recibio correctamente.

	#Para el paquete de pedir a la interfaz distribuida una pagina se ocupan los siguientes datos:
	opCode = 1
	idPagina = numP
	#Se empaquetan y se envian los datos mediante el protocolo correspondiente.
	formatoPedir = "=BB"
	packPedir = struct.pack(formatoPedir,opCode,idPagina)
	packRecibido = sendTCP(packPedir)
	#Se recibe el paquete de respuesta
	
	#opCodeR = struct.unpack("=B",packRecibido[0:1])[0]
	opCodeR = packRecibido[0]
	#En caso de que no haya error:
	#Se recibe la pagina solicitada	
	datosPagina = packRecibido[2:len(packRecibido)] # referenciar a los datos en memoria
	
	#Colocar la pagina en memoria local
	memoriaPrincipal[indPagSwap] = datosPagina # Colocar en memoria local y actualizar frame table
	pageArray[indPagSwap] = packRecibido[1] #Agrego el idPagina al pageArray

	#Si no hubo error 
	if(opCodeR == 3):
		recibido = True
	return recibido
	
def busquedaPaginaSwap(): #Sirve para localizar el indice de la pagina en la que se va a ser swap.
	global memoriaPrincipal, numeroFilasMemoria
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


def busquedaPaginaMemoriaPrincipal(numPABuscar):#Sirve para localizar el indice de la pagina que se esta buscando en memPrincipal (creo que esto ahora seria buscar en la frame table para ver adonde esta)
	global memoriaPrincipal, pageArray, numeroFilasMemoria
	indiceARetornar = -1
	paginaEncontrada = False
	i = 0
	while(i<numeroFilasMemoria and paginaEncontrada==False):
		if( pageArray[i] != -1 and pageArray[i] == numPABuscar): # Este numero de pagina ahora esta en la frame table
			indiceARetornar = i
			paginaEncontrada = True
		i += 1
	return indiceARetornar
			
			
#Habilitarle una pagina a un proceso y la coloca en la memoria principal     
def habilitarPagina():
	global numeroPagina, contadorFilaActual, numeroFilasMemoria, pageArray
	#Para cuando la memoria principal tiene filas vacias
	if (contadorFilaActual < numeroFilasMemoria): 
		pageArray[contadorFilaActual] = numeroPagina
		numeroPagina += 1
		contadorFilaActual += 1
		
	#Cuando esta llena, entonces se empieza a hacer swap.
	else:
		indMemSwap = busquedaPaginaSwap()
		guardado = False
		while (guardado == False):
			guardado = pasarPaginaLocalADistribuida(indMemSwap)
		#Agregar nueva pagina en memoria local
		pageArray[indMemSwap] = numeroPagina 
		numeroPagina += 1
	return numeroPagina-1


#Es para entregarle a la interfaz la pagina solicitada.		
def pedirPagina(numeroP):
	global memoriaPrincipal
	paginaADevolver = 0 ###Ahora es un byteArray	
	indicePaginaADevolver = busquedaPaginaMemoriaPrincipal(numeroP)
	#Esta en memoria
	if (indicePaginaADevolver != -1):
		paginaADevolver = memoriaPrincipal[indicePaginaADevolver]
	#No esta en memoria
	else:
		#Hace swap
		indMemSwap = busquedaPaginaSwap()
		guardado = False
		while (guardado == False):
			guardado = pasarPaginaLocalADistribuida(indMemSwap)# las actualizaciones del pageArray se hacen en los metodos
		recibido = False
		while (recibido == False):
			recibido = 	pasarPaginaDistribuidaALocal(indMemSwap,numeroP)
		#Se toma de la memoria local la pagina deseada
		paginaADevolver = memoriaPrincipal[indMemSwap]
		
	return paginaADevolver
	
def paginallenaMemoriaPrincipal(indiceP): #Verificar por medio de un indice si una pagina esta llena en memoria local
	global tamanoPaginaTotal, pageArray, memoriaPrincipal
	paginaLlena = False
	if(pageArray[indiceP] != -1 and len(memoriaPrincipal[indiceP]) == tamanoPaginaTotal): # Ahora esto se hace en la frame table 
		paginaLlena = True
	return paginaLlena
	
def guardar(pack,numP): #Guarda en memoria. Puede tener varias condiciones que la pagina(que le da la intefaz local) este en memoria principal pero no este llena entonces solo guarda
						#Que este en memoria principal pero la pagina esta llena y que la pagina no este en memoria principal
	global memoriaPrincipal
	numeroPag = -1 #Se retorna a la interfaz, para saber si se le habilito una nueva pagina a ese sensor o no(-1).
	indiceP = busquedaPaginaMemoriaPrincipal(numP)
	#Si esta en memoria principal
	if(indiceP != -1):
		#Reviso si la pagina esta llena.
		paginaLlena = paginallenaMemoriaPrincipal(indiceP)
		#Si tiene espacio
		if(paginaLlena == False):
			#Guarda el dato
			memoriaPrincipal[indiceP] += pack 
			
		#Si esta llena
		else:
			#Se habilita una nueva pagina
			pagNueva = habilitarPagina()
			#Ver en que posicion de memoria local quedo, y luego ya se puede guardar
			indiceP = busquedaPaginaMemoriaPrincipal(pagNueva)
			#Se guarda
			memoriaPrincipal[indiceP] += pack
			numeroPag = pagNueva
	#Si no esta en memoria local 
	else:
		indMemSwap = busquedaPaginaSwap()
		guardado = False
		while (guardado == False):
			guardado = pasarPaginaLocalADistribuida(indMemSwap)
		recibido = False
		while (recibido == False):
			recibido = pasarPaginaDistribuidaALocal(indMemSwap,numP)
		paginaLlena = paginallenaMemoriaPrincipal(indMemSwap) 
		#Si tiene espacio 
		if(paginaLlena == False):
			#Se guarda
			memoriaPrincipal[indMemSwap] += pack
		#Si esta llena
		else:
			pagNueva = habilitarPagina() 
			#Busco donde quedo
			indMemSwap = busquedaPaginaMemoriaPrincipal(pagNueva)
			#Guardo
			memoriaPrincipal[indMemSwap] += pack
			numeroPag = pagNueva
	return numeroPag
	
while(True):
	codigoLlamado = buzonLlamados.get()
	if(codigoLlamado == 0): #Llama a Habilitar pagina
		paginaHabilitada = habilitarPagina()
		buzonRetornos.put(paginaHabilitada) #Envio lo que me retorno la funcion
	elif(codigoLlamado == 1):#Llama a pedir pagina
		parametro = buzonParametros.get()
		paginaADevolver = pedirPagina(parametro)
		buzonRetornos.put(paginaADevolver)
		
	elif(codigoLlamado == 2): #Llama a guardar 
		parametro1 = buzonParametros.get()
		parametro2 = buzonParametros.get()
		numPage = guardar(parametro1,parametro2)
		contadorPrueba += 1 
		print ("ContadorPrueba: ",contadorPrueba)
		buzonRetornos.put(numPage)
	
		
			

	
			
			
			
			
		
	

