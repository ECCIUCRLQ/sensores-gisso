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
#Agregar sensor page table 
#Malloc maravilloso 
#Guardar 

def agregarSensorPageTable(sensorId,tamanoPagina):
	global pageTable,tamanoPT
	pageTable.append([])
	pageTable[tamanoPT].append(sensorId)
	nuevaPag=aMemoria.habilitarPagina(tamanoPagina)
	pageTable[tamanoPT].append(nuevaPag)
	tamanoPT+=1
	
def buscarPageTable(sensorId):
	global pageTable,tamanoPT
	encontrado=False
	numerosPagina=[]
	while(i<tamanoPT and encontrado==False):
		if(pageTable[i][0]==sensorId):
			numerosPagina=pageTable[i][1:]
			encontrado=True
	return numerosPagina
			
	
	
