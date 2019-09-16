import RPi.GPIO as GPIO
import time
from ipcqueue import sysvmq

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)


date = int( time.time() )  
q = sysvmq.Queue(2) 
  
# The input pin of the Sensor will be declared. Additional to that the pullup resistor will be activated.

print ("Sensor-Test [press ctrl+c to end it]")
  
# This output function will be started at signal detection
def callback(channel):
  if GPIO.input(channel):
    print("Signal detected")
    q.put(int(time.time()))
  else:
    q.put(0)
  
# At the moment of detecting a Signal ( falling signal edge ) the output function will be activated.
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) 
GPIO.add_event_callback(channel, callback) 
# main program loop

while True:
  time.sleep(1)
  
# Scavenging work after the end of the program
#except KeyboardInterrupt:
 #       GPIO.cleanup()

