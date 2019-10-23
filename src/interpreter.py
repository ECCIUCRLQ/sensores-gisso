# coding: utf8
import time
import datetime
import struct 

# Inicio datos/metodos temporales para testeo
formato = 'III'
datosSensor = struct.pack(formato,1,0,3) # en lugar del primer int iria int(time.time())
datosSensor2 = struct.pack(formato,2,6,2)
datosSensor3 = struct.pack(formato,2,5,3)
datosSensor4 = struct.pack(formato,4,2,2)
datosSensor5 = struct.pack(formato,7,1,1)

paginaTest = []
pagina1 = [datosSensor,datosSensor2,datosSensor3,datosSensor4,datosSensor5]
pagina2 = [datosSensor,datosSensor2,datosSensor3,datosSensor4,datosSensor5]
pagina3 = [datosSensor,datosSensor2,datosSensor3,datosSensor4,datosSensor5]
pagina4 = [datosSensor,datosSensor2,datosSensor3,datosSensor4,datosSensor5]

def reserveMemory():
	for i in range(4):
		paginaTest.append([])

def definePage():
	reserveMemory()
	paginaTest[0].append(pagina1)
	paginaTest[1].append(pagina2)
	paginaTest[2].append(pagina3)
	paginaTest[3].append(pagina4)
# Fin datos/metodos temporales para testeo

x_eje = []  # Datos que delimitan
y_eje = []	# la grafica
cantidad_y = []

# Obtiene la hora de cada paquete. Linea comentada seria la final, comentada por testeo
def getHour(packet):
	paquete = struct.unpack(formato, packet)
	#hora = time.localtime(paquete[0]).tm_hour
	hora = paquete[0]
	if hora not in x_eje:
		x_eje.append(hora)

	cantidad_y.append(hora)	# Añade la h del dato leido contado para despues saber la cantidad de veces que se llego senial
	
# Contar la cantidad de veces que se detecto senial por hora	
def contar(cantidad_y):
	contTemp = 1
	tempContados = []
	
	for i in range(len(cantidad_y)):
		for j in range(len(cantidad_y)):
			if i!=j:
				if cantidad_y[i] not in tempContados:
					if cantidad_y[i] == cantidad_y[j]:
						contTemp+=1									
		if contTemp != 1:
			tempContados.append(cantidad_y[i])
			y_eje.append(contTemp)
			contTemp=1		

# Recorre la matriz de datos paquete por paquete, llama al método para sacar la hora de cada paquete
def getData():
	for i in range(len(paginaTest)):
		for j in range(len(paginaTest[i][0])):
			getHour(paginaTest[i][0][j])	
	contar(cantidad_y)		
	x_eje.sort() # El graficador los ocupa en orden

		
def setPage():
	definePage()

def getEjeX():
	return x_eje
	
def getEjeY():
	return y_eje	
																																							
