from ipcqueue import sysvmq # Biblioteca para los buzones.
import struct
#FORMAT = 'BIBBBBBf'
buzComun = sysvmq.Queue(420)
infoUtil = struct.pack('=IIfB',2,2,57,1) #Dato a leer 1
print (infoUtil)
while(True):
	buzComun.put(infoUtil)