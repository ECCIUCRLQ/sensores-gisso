import csv
import struct
import time
import random
import administradorMemoria as aMemoria
from ipcqueue import sysvmq
pageTable=[]
tamanoPT=0
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
	
def buscarPageTable(sensorId):
	global pageTable,tamanoPT
	encontrado=False
	numerosPagina=[]
	while(i<tamanoPT and encontrado==False):
		if(pageTable[i][0]==sensorId):
			numerosPagina=pageTable[i][1:]
			encontrado=True
	return numerosPagina

def pedirDatos(sensorId):
	numerosPaginaSensor=[]
	matrizRetorno = []
	numeroPaginaSensor=buscarPageTable(sensorId)
	for i in range(0,len(numeroPaginaSensor)):
		matrizRetorno.append([])
		matrizRetorno[i].append(aMemoria.pedirPagina(numeroPaginaSensor[i])) #guardo pagina de la memoria en la matriz a retornar
	return matrizRetorno

def guardar(sensorId):

			
	
	
