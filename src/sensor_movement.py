#taken from https://electrosome.com/pir-motion-sensor-hc-sr501-raspberry-pi/

import RPi.GPIO as GPIO                           #Import GPIO library
import time 
from ipcqueue import sysvmq

                                      #Import time library
GPIO.setmode(GPIO.BCM)                          #Set GPIO pin numbering
pir = 17                                          #Associate pin 26 to pir
GPIO.setup(pir, GPIO.IN)   
q = sysvmq.Queue(2)                       #Set pin as GPIO in 

#print "Waiting for sensor to settle"
#time.sleep(2)                                     #Waiting 2 seconds for the sensor to initiate
#print "Detecting motion"


while True:
	if GPIO.input(pir):                            #Check whether pir is HIGH
		print "Motion Detected!"
		q.put(int(time.time()))
	else :
		q.put(0)  
									 #D1- Delay to avoid multiple detection
	time.sleep(1)                                #While loop delay should be less than detection(hardware) dela
