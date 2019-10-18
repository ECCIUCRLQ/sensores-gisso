import csv
import struct
import time
import random
from ipcqueue import sysvmq
#Interfaz
numeroPagina=15
memoriaPrincipal=[]
numeroFilas=13
contadorFilaActual=0
max8 = 10575
max5 = 16920
for i in range(numeroFilas):
    memoriaPrincipal.append([])

def getNumeroPagina():
		return numeroPagina 
def setNumeroPagina(x):
	 numeroPagina=x

def pasarPaginaMPrincipalSecundaria(pagSwap):
		numeroPage = memoriaPrincipal[pagSwap][0]
		nombrePagina=str(numeroPage)+".csv"
		#Se crea un archivo con los datos de la pagina seleccionada 	
		with open(nombrePagina, 'wb') as csvfile:
			filewriter = csv.writer(csvfile, delimiter=',',
						quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(memoriaPrincipal[pagSwap])
	#Esto es para borrar en memoria principal
		memoriaPrincipal[pagSwap].clear()	
#Habilitarle una pagina a un proceso y la coloca en la memoria principal     
def habilitarPagina(tamanoPagina):
	numPagina = getNumeroPagina()
	if (contadorFilaActual < 13): 
		memoriaPrincipal[contadorFilaActual].append(numeroPagina)
		numeroPagina+=1
		memoriaPrincipal[contadorFilaActual].append(tamanoPagina)
	else:
		#Swap
		pagSwapB = False
		pagSwap = -1
		while(i<13 and pagSwapB == False):
			if(memoriaPrincipal[i][1] == 5):
				if(len(memoriaPrincipal[i]) == max5):
					pagSwapB = True
					pagSwap = i
			elif(memoriaPrincipal[i][1] == 8):
				if(len(memoriaPrincipal[i]) == max8):
					pagSwapB = True
					pagSwap = i
		if(pagSwapB==False):
			pagSwap=random.randint(0,13)
		
		pasarPaginaMPrincipalSecundaria(pagSwap)
		#Agregar nueva pagina en memoria
		memoriaPrincipal[pagSwap].append(numeroPagina)
		numeroPagina += 1
		memoriaPrincipal[pagSwap].append(tamanoPagina)
	print("Hola",getNumeroPagina())
	return numPagina-1

#Es para entregarle a la interfaz la pagina solicitada.		
def pedirPagina(numeroP):
	paginaADevolver=[]
	for i in range(numeroFilas):
		#Si la pagina esta en memoria principal
		if(memoriaPrincipal[i][0]==numeroP):
			paginaADevolver = memoriaPrincipal[i][:]#Revisar esto
		#No esta en memoria
		else:
			#Swap
			pagSwapB = False
			pagSwap = -1
			while(i<13 and pagSwapB == False):
				if(memoriaPrincipal[i][1] == 5):
					if(len(memoriaPrincipal[i]) == max5):
						pagSwapB = True
						pagSwap = i
				elif(memoriaPrincipal[i][1] == 8):
					if(len(memoriaPrincipal[i]) == max8):
						pagSwapB = True
						pagSwap = i
				
			if(pagSwapB==False):
				pagSwap=random.randint(0,13)				
			
			
			pasarPaginaMPrincipalSecundaria(pagSwap)
			#Para buscar la pagina deseada en memoria principal
			arregloTemporal = []
			with open('archivo.csv', 'rb') as f:
				reader = csv.reader(f)
				for row in reader:
					arregloTemporal.append(row[0])
			 #Para colocar la pagina en memoria principal
			memoriaPrincipal[pagSwap].append(arregloTemporal)
			 
			 #Se toma de la memoria la pagina deseada
			paginaADevolver = memoriaPrincipal[pagSwap][:]
				
	return paginaADevolver
		
def guardar(pack,numP):
	paginaLlena=False
	for i in range(numeroFilas):
		#Si esta en memoria principal
		if(memoriaPrincipal[i][0]==numP):
			#Para por ver si esta llena o no
			if(memoriaPrincipal[i][1] == 5):
				if(len(memoriaPrincipal[i]) == max5):
					paginaLlena = True
			elif(memoriaPrincipal[i][1] == 8):
				if(len(memoriaPrincipal[i]) == max8):
					paginaLlena = True
			#Si tiene espacio
			if(paginaLlena==False):
				#Guarda el dato
				memoriaPrincipal[i].append(pack)
			#Si esta llena
			else:
				pagNueva = habilitarPagina(memoriaPrincipal[i][1])
				#Ver en que posicion de memoria principal quedo, y luego ya se puede guardar
				#memoriaPrincipal[].append(pack)
		else:
			#Swap
			pagSwapB = False
			pagSwap = -1
			while(i<13 and pagSwapB == False):
				if(memoriaPrincipal[i][1] == 5):
					if(len(memoriaPrincipal[i]) == max5):
						pagSwapB = True
						pagSwap = i
				elif(memoriaPrincipal[i][1] == 8):
					if(len(memoriaPrincipal[i]) == max8):
						pagSwapB = True
						pagSwap = i
				
			if(pagSwapB==False):
				pagSwap=random.randint(0,13)				
			
			pasarPaginaMPrincipalSecundaria(pagSwap)
			#Para buscar la pagina deseada en memoria principal
			arregloTemporal = []
			with open('archivo.csv', 'rb') as f:
				reader = csv.reader(f)
				for row in reader:
					arregloTemporal.append(row[0])
			 #Para colocar la pagina en memoria principal
			memoriaPrincipal[pagSwap].append(arregloTemporal)
			#Para guardar
			memoriaPrincipal[pagSwap].append(pack)
			
		
			
			
			
			
		
	
			
			
			
			
		
	
