import interpreter as interpreter

#import pandas as pd
#from matplotlib import pyplot as plt

interpreter.requestData()

ages = [52, 18, 19, 21, 25, 26, 26, 30, 32, 38, 45, 55] 
bins = interpreter.getBins()

def printPage():
	print ("Valor:", interpreter.data[0][0])

 
def graficar() : 
	print ("Printing bins")
	
	print (bins)
	
	#plt.style.use('fivethirtyeight')
	#plt.hist(ages, bins=bins, edgecolor='black')
 
	# data = pd.read_csv('data.csv')
	# ids = data['Responder_id']
	# ages = data['Age']
 
	# median_age = 29
	# color = '#fc4f30'
 
	# plt.legend()
	#plt.title('This is the title')
	#plt.title('Actividad de Sensores')
	#plt.xlabel('Tiempo (h)')
	#plt.ylabel('Promedio total de detecciones')
 
	#plt.tight_layout()
	#plt.show()
printPage()
graficar() 
