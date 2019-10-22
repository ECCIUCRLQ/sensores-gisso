import csv
import struct
import time
import random
import administradorMemoria as aMemoria
from ipcqueue import sysvmq
pageTable=[]
tamanoPT=0
FORMAT1='IBBBBf'
FORMAT2='IBBBB?'
#Pedir datos, metodo que va a llamar el graficador
#Buscar page table
#Malloc maravilloso 
#Guardar 

def mallocMaravilloso(sensorId,tamanoPagina): #Agrego en la page table y despues habilito pagina en memoria principal 
	global pageTable,tamanoPT					#Y despues meto el numero de pagina en la page table 
	pageTable.append([])
	pageTable[tamanoPT].append(sensorId)
	nuevaPag=aMemoria.habilitarPagina(tamanoPagina)
	pageTable[tamanoPT].append(nuevaPag)
	tamanoPT+=1
	#Retornar un si se agrego o no
	
def getPaginasSensor(sensorId):# Busca en la page table y retorna los numeros de pagina referentes a un sensorId
	global pageTable,tamanoPT
	encontrado=False
	numerosPagina=[]
	i=0
	while(i<tamanoPT and encontrado==False):
		if(pageTable[i][0]==sensorId):
			numerosPagina=pageTable[i][1:]
			encontrado=True
		i+=1
	return numerosPagina

def pedirDatos(sensorId): # Pido datos por medio de un sensor ID,la interfaz los va a buscar a la pagetable y se comunica con la memoria principal para retornarlos
	numerosPaginaSensor=[]
	matrizRetorno = []
	numeroPaginaSensor=getPaginasSensor(sensorId)
	for i in range(0,len(numeroPaginaSensor)):
		matrizRetorno.append([])
		matrizRetorno[i].append(aMemoria.pedirPagina(numeroPaginaSensor[i])) #guardo pagina de la memoria en la matriz a retornar
	return matrizRetorno
	
def buscarSensorId(sensorId):#Busco el sensorId en la page table y me retorna el indice
	global pageTable,tamanoPT
	indice=-1
	i=0
	while(i<tamanoPT and hallado==False):
		if(pageTable[i][0]==sensorId):
			indice=i
		i+=1
	return indice
			
def getSensorId(pack,tamanoPagina):#Desempaqueta y retorna el sensor id
	if(tamanoPagina==5):
		var = struct.unpack(FORMAT2,data) # Desempaqueta los datos recibidos
		sensorId=var[0]
	else:
		var = struct.unpack(FORMAT1,data) # Desempaqueta los datos recibidos
		sensorId=var[0]
	return sensorId
	
def datoUtil(pack,tamanoPagina):#Desempaqueta y retorna fecha y dato en un paquete
	if(tamanoPagina==5):
		var = struct.unpack(FORMAT2,data) # Desempaqueta los datos recibidos
		packUtil=struct.pack('BBBBf',var[1],var[2],var[3],var[4],var[5])
	else:
		var = struct.unpack(FORMAT1,data) # Desempaqueta los datos recibidos
		packUtil=struct.pack('BBBB?',var[1],var[2],var[3],var[4],var[5])
	return packUtil
	 


def guardar(pack,tamanoPagina):#Busca el sensor ID, sino esta entonces lo agrega a la page table y luego guarda los datos en memoria.i
	global pageTable
	ind=buscarSensorId(getSensorId(pack,tamanoPagina))
	if(ind==-1):
		mallocMaravilloso(getSensorId(pack,tamanoPagina),tamanoPagina)
	packDatos=datoUtil(pack,tamanoPagina)
	numP=aMemoria.guardar(packDatos)
	if(numP!=-1):
		pageTable[ind].append(numP)
	
		
		
		
	
	

			
	
	
