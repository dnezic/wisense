#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, time
import dhtreader
import zmq


AM2302 = 22

dhtreader.init()

dev_type = AM2302
dhtpin = 22

x = None
i = 0

port_lcd = sys.argv[1]
port_hub = sys.argv[2]

while x == None and i < 10:
   x = dhtreader.read(dev_type, dhtpin)
   if x != None:
      t, h = x
      if t and h:
          
         data = "{0:.1f}C {1:d}%".format(t, int(h))
         out = "{0:.1f}:{1:d}".format(t, int(h))
         data = data.ljust(10, " ")         
         id = "WS"
         context = zmq.Context()
         socket = context.socket(zmq.REQ)
         socket.linger = 1000
         socket.connect ("tcp://localhost:%s" % port_lcd)
         socket.send(bytes(id+"16"+data, 'ascii'), zmq.NOBLOCK)
         
         socket = context.socket(zmq.REQ)
         socket.linger = 1000
         socket.connect ("tcp://localhost:%s" % port_hub)
         socket.send(bytes("DHT22"+out, 'ascii'), zmq.NOBLOCK)

   i = i + 1
   time.sleep(0.5)


