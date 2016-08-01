#!/usr/bin/python3
"""
   Send current time to LCD if daemon exists
"""

import zmq
import sys
import time



id = "CLOCK"
port = sys.argv[1]
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
t = time.strftime("%H:%M")
socket.send(bytes(id+t, 'ascii'), zmq.NOBLOCK)
socket.linger = 1000
