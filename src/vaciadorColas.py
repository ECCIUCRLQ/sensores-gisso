import struct
import random
from ipcqueue import sysvmq
buzonGeneral=sysvmq.Queue(420)#Buzon para procesos recolectores
buzonLlamados=sysvmq.Queue(17)#Buzon para solicitar al administrador meter datos.
buzonRetornos=sysvmq.Queue(16)#Buzon para recibir la respuesta del administrador.
buzonParametros=sysvmq.Queue(15)
buzonShock = sysvmq.Queue(1)
buzonMov = sysvmq.Queue(2)
buzonLlamadoGraficador = sysvmq.Queue(69)
while(True):
	try:
		buzonGeneral.get_nowait()
	except:
		pass
	try:
		buzonLlamados.get_nowait()
	except:
		pass
	try:
		buzonRetornos.get_nowait()
	except:
		pass
	try:	
		buzonParametros.get_nowait()
	except:
		pass
	try:	
		buzonShock.get_nowait()
	except:
		pass
	try:	
		buzonMov.get_nowait()
	except:
		pass
	try:
		buzonLlamadoGraficador.get_nowait()
	except:
		pass		
		
		

