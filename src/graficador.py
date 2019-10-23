import interpreter as interpreter
import matplotlib.pyplot as plt 

def setup():
	interpreter.setPage()
	interpreter.getData()
	
	# x-coordinates of left sides of bars  
	left = interpreter.getEjeX()
	
	# heights of bars 
	height = interpreter.getEjeY() 
	
	# plotting a bar chart
	plt.bar(left, height, width = 0.8, color = ['red', 'green']) 
	 
def graficar():  
	setup()
	
	# naming the axis 
	plt.xlabel('Hora(s)') 
	plt.ylabel('# Detecciones') 
	
	# plot title 
	plt.title('Actividad de sensores') 
  
	# function to show the plot 
	plt.show() 


graficar()
