import csv
import struct
import time
import random
from ipcqueue import sysvmq
import pdb
numeroPagina=0
memoriaPrincipal=[]
numeroFilas=13
contadorFilaActual=0
#max8 = 10575
#max5 = 16920
max8 = 8
max5 = 8
buzonLlamados=sysvmq.Queue(17)
buzonRetornos=sysvmq.Queue(16)
buzonParametros=sysvmq.Queue(15)
#HabilitarPagina = 0
#pedirPagina =1
#guardar=2
for i in range(numeroFilas):
    memoriaPrincipal.append([])

def pasarPaginaMPrincipalSecundaria(pagSwap):
	global memoriaPrincipal
	numeroPage = memoriaPrincipal[pagSwap][0]
	nombrePagina=str(numeroPage)+".csv"
	#Se crea un archivo con los datos de la pagina seleccionada 	
	with open(nombrePagina, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',',
					quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(memoriaPrincipal[pagSwap])
	#Esto es para borrar en memoria principal
	del memoriaPrincipal[pagSwap][:]
	
	
def pasarPaginaMSecundariaPrincipal(pagSwap,numP):
	global memoriaPrincipal
	#Para buscar la pagina deseada en memoria principal
	arregloTemporal = []
	nombrePagina=str(numP)+".csv"
	with open(nombrePagina, 'rb') as csvfile:
		arregloTemporal = list(csv.reader(csvfile))
	 #Para colocar la pagina en memoria principal
	memoriaPrincipal[pagSwap]=arregloTemporal[0][:]#.append(arregloTemporal[0])
	print(arregloTemporal[0][1])
	print(memoriaPrincipal[pagSwap])
	print(memoriaPrincipal[pagSwap][0])
	
	
def busquedaPaginaSwap():
	global memoriaPrincipal,max5,max8
	pagSwapB = False
	indMemSwap = -1
	i=0
	while(i<13 and pagSwapB == False):
		if(len(memoriaPrincipal[i])>0 and memoriaPrincipal[i][1] == 5):
			if(len(memoriaPrincipal[i]) == max5):
				pagSwapB = True
				indMemSwap = i
		elif(len(memoriaPrincipal[i])>0 and memoriaPrincipal[i][1] == 8):
			if(len(memoriaPrincipal[i]) == max8):
				pagSwapB = True
				indMemSwap = i
		i+=1
	if(pagSwapB==False):
		vacio=True
		while(vacio==True):
			indMemSwap=random.randint(0,12)
			if(len(memoriaPrincipal[indMemSwap])>0):
				vacio=False
		
	return indMemSwap


def busquedaPaginaMemoriaPrincipal(numPABuscar):
	global memoriaPrincipal
	indiceARetornar=-1
	paginaEncontrada=False
	i=0
	while(i<13 and paginaEncontrada==False):
		if(len(memoriaPrincipal[i]) > 0 and memoriaPrincipal[i][0]==numPABuscar):
			indiceARetornar=i
			paginaEncontrada=True
		i+=1
	return indiceARetornar
			
			
#Habilitarle una pagina a un proceso y la coloca en la memoria principal     
def habilitarPagina(tamanoPagina):
	global numeroPagina, contadorFilaActual,memoriaPrincipal,max5,max8
	if (contadorFilaActual < 13): 
		memoriaPrincipal[contadorFilaActual].append(numeroPagina)
		numeroPagina+=1
		memoriaPrincipal[contadorFilaActual].append(tamanoPagina)
		contadorFilaActual+=1
	else:
		indMemSwap=busquedaPaginaSwap()
		pasarPaginaMPrincipalSecundaria(indMemSwap)
		#Agregar nueva pagina en memoria
		memoriaPrincipal[indMemSwap].append(numeroPagina)
		numeroPagina += 1
		memoriaPrincipal[indMemSwap].append(tamanoPagina)
	return numeroPagina-1


#Es para entregarle a la interfaz la pagina solicitada.		
def pedirPagina(numeroP):
	global memoriaPrincipal,numeroFilas,max5,max8
	paginaADevolver=[]
	for i in range(numeroFilas):
		#Si la pagina esta en memoria principal
		if(memoriaPrincipal[i][0]==numeroP):
			paginaADevolver = memoriaPrincipal[i][:]#Revisar esto
		#No esta en memoria
		else:
			indMemSwap=busquedaPaginaSwap()
			pasarPaginaMPrincipalSecundaria(indMemSwap)
			
			pasarPaginaMSecundariaPrincipal(pagSwap,numeroP)
			 #Se toma de la memoria la pagina deseada
			paginaADevolver = memoriaPrincipal[indMemSwap][:]
	return paginaADevolver
	
def paginallenaMemoriaPrincipal(indiceP):
	print("aqui me caigo")
	paginaLlena=False
	print("Ind:" + str(indiceP))
	print ("Tamano de celdas pagina" + str(memoriaPrincipal[indiceP][1]))
	print ("Tamano" + str(len(memoriaPrincipal[indiceP])))
	if(memoriaPrincipal[indiceP][1] == 5):
		#print("Entre al if que es")
		if(len(memoriaPrincipal[indiceP]) == max5):
			#print("Entre a if que dice que si esta llena")
			paginaLlena = True
	elif(memoriaPrincipal[indiceP][1] == 8):
		if(len(memoriaPrincipal[indiceP]) == max8):
			paginaLlena = True
	#print("Retorna pagina llena con" + str(paginaLlena))
	return paginaLlena
	
def guardar(pack,numP):
	global numeroFilas, memoriaPrincipal,max5,max8
	numeroPag=-1
	indiceP=busquedaPaginaMemoriaPrincipal(numP)
	print(indiceP)
	#Si esta en memoria principal
	if(indiceP!=-1):
		#print("Se llama a paginaLlena con indice" + str(indiceP))
		paginaLlena=paginallenaMemoriaPrincipal(indiceP)
		#Si tiene espacio
		#print ("Pagina llena de guardar " + str(paginaLlena))
		if(paginaLlena==False):
			#Guarda el dato
			memoriaPrincipal[indiceP].append(pack)
		#Si esta llena
		else:
			#print ("Esta entrando al else que dice que esta llena")
			pagNueva = habilitarPagina(memoriaPrincipal[indiceP][1])
			#Ver en que posicion de memoria principal quedo, y luego ya se puede guardar
			indiceP=busquedaPaginaMemoriaPrincipal(pagNueva)
			memoriaPrincipal[indiceP].append(pack)
			numeroPag=pagNueva
	#Si no esta en memoria principal
	else:
		#print("Entre al else")
		indMemSwap=busquedaPaginaSwap()
		#print("Indice swap:" + str(indMemSwap))
		pasarPaginaMPrincipalSecundaria(indMemSwap)
		pasarPaginaMSecundariaPrincipal(indMemSwap,numP)
		paginaLlena=paginallenaMemoriaPrincipal(indMemSwap)
		if(paginaLlena==False):
			#Para guardar
			memoriaPrincipal[indMemSwap].append(pack)
		else:
			#print ("Esta entrando al otro else en donde se dice que la pagina esta llena")
			pagNueva=habilitarPagina(memoriaPrincipal[indMemSwap][1])
			indMemSwap=busquedaPaginaMemoriaPrincipal(pagNueva)
			memoriaPrincipal[indMemSwap].append(pack)
			numeroPag=pagNueva
	return numeroPag
	
while(True):
	codigoLlamado=buzonLlamados.get()
	if(codigoLlamado==0):
		parametro=buzonParametros.get()
		paginaHabilitada=habilitarPagina(parametro)
		buzonRetornos.put(paginaHabilitada)
	elif(codigoLlamado==1):
		parametro=buzonParametros.get()
		paginaADevolver=pedirPagina(parametro)
		buzonRetornos.put(paginaADevolver)
		
	elif(codigoLlamado==2):
		parametro1=buzonParametros.get()
		parametro2=buzonParametros.get()
		numPage=guardar(parametro1,parametro2)
		buzonRetornos.put(numPage)
	
		
			

	
			
			
			
			
		
	

