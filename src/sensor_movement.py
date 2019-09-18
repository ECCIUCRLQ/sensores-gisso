#Taken from https://electrosome.com/pir-motion-sensor-hc-sr501-raspberry-pi/

import RPi.GPIO as GPIO                         # Biblioteca para detectar los pines del Pi
import time 
from ipcqueue import sysvmq						# Biblioteca para el buzon

                                    
GPIO.setmode(GPIO.BCM)                        	  # Numeros del GPIO del pin
pir = 17                                          # Asociar pin 17 a pir
GPIO.setup(pir, GPIO.IN)   						  # Asignar el pin
q = sysvmq.Queue(2)                     		  # Crea el buzon con la llave 2

while True:
	if GPIO.input(pir):   						# Si detecto actividad en ese pin                        
		print "Motion Detected!"
		q.put(int(time.time()))					# Agrega el tiempo en que se detecto al buzon
	else :
		q.put(0)  								# Agrega 0 al buzon indicando que no se detecto movimiento, seria el keepalive
									
	time.sleep(1)                              	# Espera 1 segundo.
