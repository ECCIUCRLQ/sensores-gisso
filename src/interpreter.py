# coding: utf8
import time
import datetime
import struct 
from ipcqueue import sysvmq
formatoFloat = 'If'
formatoInt = 'II'
formatoBool = 'IB'
matrizRetorno = []
buzonLlamadoGraficador=sysvmq.Queue(69)
buzonRetornoGraficador=sysvmq.Queue(469)


x_eje = []  # Datos que delimitan
y_eje = []	# la grafica

cantidad_y = []
datos_y = []

tipoDato = 0


# Obtiene la hora de cada paquete. Linea comentada seria la final, comentada por testeo
def getHour(packet):
	global tipoDato
	print ("TIPO DATO: ",tipoDato)
	formato = formatoBool
	if(tipoDato == 1):
		formato = formatoBool
	elif (tipoDato == 2):
		formato = formatoInt		
	
	paquete = struct.unpack(formato, packet)
	hora = time.localtime(paquete[0]).tm_min
	#hora = paquete[0]
	dato = paquete[1]
	if hora not in x_eje:
		x_eje.append(hora)

	cantidad_y.append(hora)	# Añade la h del dato leido contado para despues saber la cantidad de veces que se llego senial
	if (tipoDato != 3):
		datos_y.append(dato)

# Contar la cantidad de veces que se detecto senial por hora	
def contar(cantidad_y):
	tempContados = []
	esBool = isBool()
	
	for i in range(len(cantidad_y)):
		contadorProm = 1
		if esBool:
			contTemp = 1
		else:	
			contTemp = datos_y[i]
			
		for j in range(len(cantidad_y)):
			if i!=j:
				if cantidad_y[i] not in tempContados:
					if cantidad_y[i] == cantidad_y[j]:	
						if esBool:
							contTemp+=1
						else:
							contTemp+=datos_y[j]
							contadorProm+=1
									
							 							
		if cantidad_y[i] not in tempContados:
			tempContados.append(cantidad_y[i])
			if (esBool == False):
				contTemp/=contadorProm
			y_eje.append(contTemp)

# Recorre la matriz de datos paquete por paquete, llama al método para sacar la hora de cada paquete
def getData():
	print("len",matrizRetorno)
	for i in range(len(matrizRetorno)):
		for j in range(2,len(matrizRetorno[i][0])):
			print
			getHour(matrizRetorno[i][0][j])	
	contar(cantidad_y)		
	x_eje.sort() # El graficador los ocupa en orden
	print("x_eje", x_eje)
	print("y_eje", y_eje)
	print("cantidad_y", cantidad_y)
	print("datos_y", datos_y)
		
# tipoDato=1 float 
# tipoDato=2 int 
# tipoDato=else bool 
		
def setPage(equipoId,sensorId):
	iD = str(equipoId)+str(sensorId)
	iD = int(iD)
	print("ID: ",iD)
	global matrizRetorno,tipoDato
	buzonLlamadoGraficador.put(iD)
	matrizRetorno=buzonRetornoGraficador.get()
	print("Retorno: ",matrizRetorno)
	
	if (equipoId == 5 and sensorId == 2):
		tipoDato = 1 # float
	elif (equipoId == 6):
		tipoDato = 2 # int
	else:
		tipoDato = 3 # bool	
	
	getData()
	
def getEjeX():
	return x_eje
	
def getEjeY():
	return y_eje	
																																							
def isBool():
	if tipoDato == 3:
		return True
	return False
	
