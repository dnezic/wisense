import zmq
import sys

port = 5000
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
socket.send(b"WS10text is this", zmq.NOBLOCK)
socket.linger = 1000

