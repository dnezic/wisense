"""
   Send current time to LCD if daemon exists
"""

import zmq
import sys
import time

time.sleep(30)


id = "WS"
port = sys.argv[1]
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
s = id+"ST"
socket.send(bytes(s, 'ascii'), zmq.NOBLOCK)
socket.linger = 1000



socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
t = time.strftime("%H:%M")
t = t.ljust(32, ' ')
socket.send(bytes(id+"10"+t, 'ascii'), zmq.NOBLOCK)
socket.linger = 1000

time.sleep(10)

socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
s = id+"RE"
socket.send(bytes(s, 'ascii'), zmq.NOBLOCK)
socket.linger = 1000
