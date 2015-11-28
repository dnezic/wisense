#!/usr/bin/python3

import sys
import threading
import zmq
import socket
import time
from time import gmtime, strftime
import sqlite3

port = sys.argv[1]
db_path = sys.argv[2]


def route(message):
    id = message[:5].lower()
    data = message[5:]

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    if id == 'dht22':
        t = data.split(":")[0]
        h = data.split(":")[1]
        c.execute("INSERT INTO sensors_dht22 VALUES (NULL,'" + tm + "'," + str(t) + "," + str(h) + ")")
    elif id == 'bme28':
        t = data.split(":")[0]
        h = data.split(":")[1]
        p = data.split(":")[2]
        c.execute("INSERT INTO sensors_bme280 VALUES (NULL,'" + tm + "'," + str(t) + "," + str(h) + "," + str(p) + ")")
    elif id == 'rf24l':
        voltage = data.split(":")[1]
        t = data.split(":")[2]
        p = data.split(":")[3]
        ccc = data.split(":")[4]
        i2c_e = data.split(":")[5]
        c.execute("INSERT INTO sensors_rf24l VALUES (NULL," + str(voltage) + "," + str(ccc) + ",'" + tm + "'," + str(t) + "," + str(p)+ "," + str(i2c_e) + ")")

    conn.commit()
    conn.close()

while True:
   context = zmq.Context()
   socket = context.socket(zmq.REP)
   socket.bind("tcp://*:" + port)
   message = socket.recv()
   message = message.decode('utf-8', 'ignore')
   print(message)

   route(message)


   socket.send(b"\0")
