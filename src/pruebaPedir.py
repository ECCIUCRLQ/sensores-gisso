import time 
from ipcqueue import sysvmq

i = 0
buzonLlamadoGraficador = sysvmq.Queue(69)
while (i < 5):
    buzonLlamadoGraficador.put(i)
    i += 1
    time.sleep(5)
