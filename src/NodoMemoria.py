import sys
import time

#Metadatos Generales:
#-Puntero final de metadatos 4 bytes
#-Puntero final de datos 4 bytes

#Metadatos de cada dato:
#-ID 1 bytes
#-Tamaño pagina 4 bytes
#-Puntero donde inician los datos 4 bytes
#-Fecha Modificacion 4 bytes
#-Fecha Consulta 4 bytes
punteroMeta = 0
punteroDatos = 4

if( len(sys.argv) < 4 ):
	print ("NodoMemoria: Error, argumentos insuficientes")
	exit()

tamanoMax = int(sys.argv[1])
tamanoDisponible = tamanoMax

def crearArchivo():
	global tamanoMax
	global punteroMeta
	global punteroDatos
	
	archivo = open("nodoMemoria.bin", 'bw')
	archivo.seek(punteroMeta)
	puntM = 8
	puntD = tamanoMax
	archivo.write(puntM.to_bytes(4,byteorder = 'big'))
	archivo.seek(punteroDatos)
	archivo.write(puntD.to_bytes(4,byteorder = 'big'))
	archivo.close()
	
def tamDisponible()
	global tamanoMax
	global tamanoDisponible
	
	if(tamanoMax == tamanoDisponible):
		tamanoDisponible -= 25
	
	else:
		tamanoDisponible -= 17
		
	return tamanoDisponible
	
def agregarMetadatos(idPagina,tamPagina):
	archivo = open("nodoMemoria.bin", 'br+')
	archivo.seek(punteroMeta)
	escribiendoMeta = int.from_bytes(archivo.read(4), byteorder = 'big')
	
	archivo.seek(punteroDatos)
	escribiendoDatos = int.from_bytes(archivo.read(4), byteorder = 'big')
	
	archivo.seek(escribiendoMeta)
	archivo.write(idPagina.to_bytes(1,byteorder = 'big'))
	archivo.write(tamPagina.to_bytes(4,byteorder = 'big'))
	
	escribiendoDatos -= tamPagina
	archivo.write(escribiendoDatos.to_bytes(4,byteorder = 'big'))
	
	fechaCreacion = int(time.time())
	archivo.write(fechaCreacion.to_bytes(4,byteorder = 'big'))
	archivo.write(fechaCreacion.to_bytes(4,byteorder = 'big'))
	
	escribiendoMeta += 17
	archivo.seek(punteroMeta)
	archivo.write(escribiendoMeta.to_bytes(4,byteorder = 'big'))
	archivo.seek(punteroDatos)
	archivo.write(escribiendoDatos.to_bytes(4,byteorder = 'big'))
	
	archivo.close()
	
	return escribiendoDatos
	
	
def agregarDatos(datos):
	global tamanoDisponible
	
	escribiendo = agregarMetadatos(datos[0],datos[1])
	archivo = open("nodoMemoria.bin", 'br+')
	archivo.seek(escribiendo)
	archivo.write(datos[2]) #####Aqui falta ver el formato de los datos y ver cuales guardar
	archivo.close()
	
	tamanoDisponible -= datos[1]
	
def buscarDatos(idPagina)
	global punteroMeta
	
	inicioDatos = -1
	indice = 8
	identificador = -1
	terminar = False
	datosCompletos = -1
	archivo = open("nodoMemoria.bin", 'br+')
	archivo.seek(punteroMeta)
	finMeta = int.from_bytes(archivo.read(4), byteorder = 'big')
	while(terminar == False and indice < finMeta):
		archivo.seek(indice)
		identificador = int.from_bytes(archivo.read(1), byteorder = 'big')
		if(identificador == idPagina):
			terminar = True
			archivo.seek(indice+1)
			tam = int.from_bytes(archivo.read(4), byteorder = 'big')
			archivo.seek(indice+5)
			inicioDatos = int.from_bytes(archivo.read(4), byteorder = 'big')
			archivo.seek(inicioDatos)
			datosCompletos = archivo.read(tam)
			
		else:
			indice += 17
	
	return datosCompletos
	
	


