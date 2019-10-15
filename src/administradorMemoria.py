import struct
import time
import random
from ipcqueue import sysvmq
#Interfaz
numeroPagina = 0
memoriaPrincipal=[]
numeroFilas=13
contadorFilaActual=0
max8 = 10575
max5 = 16920
for i in range(numeroFilas):
    memoriaPrincipal.append([])
    
def pedirPagina(tamanoPagina):
	if (contadorFilaActual < 13):
		memoriaPrincipal[contadorFilaActual].append(numeroPagina)
		numeroPagina += 1
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
		#crear un archivo nuevo 
			
		if(pagSwapB==False):
			pagSwap=random.randint(0,13)
		
		#Se crea un archivo con los datos de la pagina seleccionada 	
		archivo = open("datos.txt","w") # Tenemos que crear archivos para cada uno.
		archivo.write(aEscribir) # Escribimos en archivo
		archivo.close()
		#Esto es para borrar en memoria principal
		memoriaPrincipal[pagSwap].clear()
		#Agregar nueva pagina en memoria
		memoriaPrincipal[contadorFilaActual].append(numeroPagina)
		numeroPagina += 1
		memoriaPrincipal[contadorFilaActual].append(tamanoPagina)
		
		return numeroPagina-1
		
		
		
			
			
		
			
			
			
			
		
	
