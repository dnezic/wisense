"""
   Send current time to LCD if daemon exists
"""

import zmq
import sys
import time
import psutil

time.sleep(10)
 
id = "CP"
port = sys.argv[1]

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
s = id+"ST"
socket.send(bytes(s, 'ascii'), zmq.NOBLOCK)
socket.linger = 1000

for x in range(10):
   load = psutil.cpu_percent(interval=2, percpu=False)
   cpu_temp = 0
   with open("/sys/class/thermal/thermal_zone0/temp") as f:
       cpu_temp = str(round(float(f.read())/1000, 1))
   payload = "CPU: " + str(load) + "% " + cpu_temp + "C"
   payload = payload.ljust(16, ' ')
   payload += (int)(16*(load/100.0))*'|'
   payload = payload.ljust(32, ' ')
   s = id+"10"+payload   
   socket = context.socket(zmq.REQ)
   socket.connect ("tcp://localhost:%s" % port)   
   socket.send(bytes(s, 'ascii'), zmq.NOBLOCK)
   socket.linger = 1000

socket = context.socket(zmq.REQ)   
socket.connect ("tcp://localhost:%s" % port)
s = id+"RE"
socket.send(bytes(s, 'ascii'), zmq.NOBLOCK)
socket.linger = 1000
