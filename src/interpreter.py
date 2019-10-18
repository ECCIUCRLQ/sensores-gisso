# coding=utf-8

#import pagetable as page

 #este sería mi variable local con todos los datos de la lista de listas
paginaTest = []
pagina1 = [1,2,3,4,5]
pagina2 = [6,7,8,9,10]
pagina3 = [11,12,13,14,15]
pagina4 = [16,17,18,19,20]

globlaxd ="hola" 

def setPage():
	for i in range(len(pagina1)):
		paginaTest.append([])

def definePage():
	setPage()
	paginaTest[0].append(pagina1)
	paginaTest[1].append(pagina2)
	paginaTest[2].append(pagina3)
	paginaTest[3].append(pagina4)


def requestData(): #'sensor' como parámetro
	#data = page.getData(sensor) - > se llama a la pageTable para obtener todos los datos de un sensor, me tiene que devolver una lista de listas
	definePage()
		
def getPage():
	return paginaTest

data = getPage()

def getBins():
	#temp = [0,0,0,0,0]
	
	temp = data[1][0]
		
	return temp
		
	
