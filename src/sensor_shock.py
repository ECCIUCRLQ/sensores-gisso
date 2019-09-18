import RPi.GPIO as GPIO
import time
from ipcqueue import sysvmq

pir = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir, GPIO.IN)


date = int( time.time() )  
q = sysvmq.Queue(1) 						# Crea el buzon con la llave 1

while True:
  if GPIO.input(pir):						# Si detecto actividad en ese pin  
    print("Signal detected")
    q.put(int(time.time()))					# Agrega el tiempo en que se detecto al buzon
  else:
    q.put(0)								# Agrega 0 al buzon indicando que no se detecto movimiento, seria el keepalive
    
  time.sleep(1)								# Espera 1 segundo.
  
