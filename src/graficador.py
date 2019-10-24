# Librerias necesarias:
#	sudo apt install python-pip
#	sudo pip install matploblib
#	sudo apt install python-tk

import interpreter as interpreter
import matplotlib.pyplot as plt 

import sys

suficiente = True

def setup():
	global suficiente
	teamID = sys.argv[1]
	sensorID = sys.argv[2]
	
	print("ids",teamID,sensorID)
	
	interpreter.setPage(teamID,sensorID)
	#interpreter.getData()
	
	# x-coordinates of left sides of bars  
	left = interpreter.getEjeX()
	
	# heights of bars 
	height = interpreter.getEjeY() 
	
	if(len(left) == 0 or len(height) == 0):
		suficiente = False
		print("No hay datos suficientes")
	
	# plotting a bar chart
	
	plt.bar(left, height, width = 0.8, color = ['red'], ) # label = 
	#pylab.legend(loc='upper left') pos de la etiqueta
	 
def graficar():
	global suficiente  
	setup()
	
	# naming the axis 
	plt.xlabel('Minuto(s)')
	if interpreter.isBool(): 
		plt.ylabel('Cantidad de Detecciones') 
	else:
		plt.ylabel('Promedio de Datos') 
	# plot title 
	plt.title('Actividad de sensores') 
  
	# function to show the plot 
	if(suficiente):
		plt.show() 


graficar()
