from ipcqueue import sysvmq # Biblioteca para los buzones.
import struct
#FORMAT = 'BIBBBBBf'
buzComun = sysvmq.Queue(420)
infoUtil = struct.pack('=IIfB',2,2,57,1) #Dato a leer 1
print (infoUtil)
i = 0
while(i<41):
	buzComun.put(infoUtil)
	i+=1
