# coding: utf8
import struct
import time
import random
from ipcqueue import sysvmq
import threading
pageTable = []
tamanoPT = 0 #Tamano page table
FORMAT = '=IIfB' # IdentificadorSensor,fecha, dato,bit para verificar dato. 

buzonGeneral = sysvmq.Queue(420)#Buzon para procesos recolectores
buzonLlamados = sysvmq.Queue(17)#Buzon para solicitar al administrador meter datos.
buzonRetornos = sysvmq.Queue(16)#Buzon para recibir la respuesta del administrador.
buzonParametros = sysvmq.Queue(15)
buzonLlamadoGraficador = sysvmq.Queue(69)
buzonRetornoGraficador = sysvmq.Queue(469)

	
def mallocMaravilloso(sensorId): #Agrego en la page table y despues habilito pagina en memoria principal 
	global pageTable,tamanoPT					#Y despues meto el numero de pagina en la page table 
	pageTable.append([])
	pageTable[tamanoPT].append(sensorId)
	buzonLlamados.put(0) #Para llamar a habilitarPagina()
	print("Llame al habilitar")
	nuevaPag = buzonRetornos.get() 
	#Agrego la nueva pagina a la page table
	pageTable[tamanoPT].append(nuevaPag)
	tamanoPT += 1
	print("PageTable ",pageTable)
	
def getPaginasSensor(sensorId):# Busca en la page table y retorna los numeros de pagina referentes a un sensorId, lo utiliza pedirDatos()
	global pageTable,tamanoPT
	encontrado = False
	numerosPagina = []
	i = 0
	while(i < tamanoPT and encontrado == False):
		if(pageTable[i][0] == sensorId):
			numerosPagina = pageTable[i][1:]
			encontrado = True
		i += 1
	return numerosPagina

#Para obtener el tamano de los paquetes
def getTamanoPaquete(sensor): #Retorna el tamaño de celda en la memoria principal, si en el pack el dato del sensor es booleano entonces devuelve un cinco o sino un ocho
	tamanoPaquete = 5
	if(sensor==52 or sensor==53 or sensor==61 or sensor==62):
		tamanoPaquete = 8
	return tamanoPaquete

def pedirDatos(sensorId): # Pido datos por medio de un sensor ID,la interfaz los va a buscar a la pagetable y se comunica con la memoria principal para retornarlos
	numerosPaginaSensor = []
	matrizRetorno = []
	tamanoPaquetesSensor = getTamanoPaquete(sensorId)
	numeroPaginaSensor = getPaginasSensor(sensorId)
	#Voy pidiendo cada una de las paginas
	for i in range(0,len(numeroPaginaSensor)):
		matrizRetorno.append([])
		buzonLlamados.put(1) #Para llamar a pedirPagina
		buzonParametros.put(numeroPaginaSensor[i]) #Se le pasa la id de pagina por parametro.
		#Recibo pagina en forma de un bytearray
		paginaAMeter = buzonRetornos.get()
		#Para convertir el bytearray a un array
		arregloTemporal = []
		j = 0	
		while(j<len(paginaAMeter)):
			arregloTemporal.append(paginaAMeter[j:j+tamanoPaquetesSensor+1])
		j += tamanoPaquetesSensor+1		

		matrizRetorno[i].append(arregloTemporal)
	
	buzonRetornoGraficador.put(matrizRetorno)
	
def buscarSensorId(sensorId):#Busco el sensorId en la page table y me retorna el indice
	global pageTable,tamanoPT
	indice = -1
	i = 0
	hallado = False
	while(i<tamanoPT and hallado==False):
		if( pageTable[i][0] == sensorId ):
			indice = i
		i += 1
	return indice
			
def getSensorId(pack):#Desempaqueta y retorna el sensor id
	var = struct.unpack(FORMAT,pack) # Desempaqueta los datos recibidos
	identificador = var[0]
	return identificador
	
def datoUtil(pack):#Desempaqueta y retorna fecha y dato en un paquete
	var = struct.unpack(FORMAT,pack) # Desempaqueta los datos recibidos
	#print("Arreglo de Paquete desempaquetado",var)
	datoAleer = var[3]
	packUtil = 0
	if(datoAleer == 0):
		packUtil = struct.pack('=IB',var[1],var[2])
	elif(datoAleer == 1):
		packUtil = struct.pack('=II',var[1],((int)(var[2])) )
	elif(datoAleer == 2):
		packUtil = struct.pack('=If',var[1],var[2])
		
	#print("Contenido packUtil: ",packUtil)
	return packUtil



###Se debe cambiar, pero creo que se podria primero ver como van a quedar los metodos del administrador
					#Se le pasa un pack, este se le busca el sensorID
def guardar(pack):#Busca el sensor ID, sino esta entonces lo agrega a la page table y luego guarda los datos en memoria.
	global pageTable
	ind = buscarSensorId(getSensorId(pack))
	if(ind == -1):
		print("Llamo a Malloc")
		mallocMaravilloso(getSensorId(pack)) 
	packDatos = datoUtil(pack)
	buzonLlamados.put(2) #Para llamar a guardar()
	buzonParametros.put(packDatos) #Para pasar el pack por parametro
	buzonParametros.put(pageTable[ind][len(pageTable[ind])-1]) #Para pasar el idPagina actual asociado a ese sensor.
	numP = buzonRetornos.get()
	#Si le habilito a el sensor una pagina nueva
	if(numP != -1):
		#Se agrega la pagina a la page table.
		pageTable[ind].append(numP)
		print("Agregue una nueva pagina")
		print ("PageTable: ",pageTable)
		
	
	
while(True):
	packRecolector = -1
	try:											#Recoge lo que tenga el buzon de los procesos recolectores y o guarda en pack recolector.
		packRecolector = buzonGeneral.get_nowait() # get_nowait() revisa el buzon, si esta vacio no pasa nada, y sino recibe el dato para enviarlo
	except:
		pass	
	if 	(packRecolector != -1): # Si pack recolector es distinto de -1 lo guarda
		#Esta llegando el mismo paquete (de prueba.py)
		#print (packRecolector)
		guardar(packRecolector)
	sID = -1
	try:
		sID = buzonLlamadoGraficador.get_nowait() #Buzón graficador recoge lo que le envie el graficador y lo guarda en sID 
	except:										#Si SID es distinto de -1 entonces pide los datos referentes a ese sensorID
		pass
	if(sID != -1):
		pedirDatos(sID)
	#time.sleep(1)
		
