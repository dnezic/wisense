#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, time, os
from quick2wire.i2c import I2CMaster, writing_bytes, reading
import zmq

port_lcd = sys.argv[1]
port_hub = sys.argv[2]

DEV = 0x51
PORT = 1
TEMP = 10

class i2c:        
        def __init__(self, port, addr, debug = False):
                self.i2c_device = I2CMaster(port)
                self.addr = addr                
                self.debug = debug
                
        def write_byte(self, *bytes):
                self.i2c_device.transaction(
                        writing_bytes(self.addr, *bytes))
                                
        def read_byte(self, register):
                byte = self.i2c_device.transaction(
                        writing_bytes(self.addr, register),
                        reading(self.addr, 1))[0][0]
                return byte
bus = i2c(1, 0x51)

t_i = int(bus.read_byte(10))
t_d = int(bus.read_byte(11))
h_i = int(bus.read_byte(12))
h_d = int(bus.read_byte(13))
error = int(bus.read_byte(14))

if error != 0:
    print("DHT error reading: ", error)

temp = t_i + float(t_d / 100.0)
hum = h_i + float(h_d / 100.0)

t, h = temp, hum
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


