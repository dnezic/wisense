#!/usr/bin/python3

import sys
import threading
import zmq
import socket
import time

from threading import Thread
from time import gmtime, strftime
from datetime import datetime

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont, ImageDraw

messages = {}
lock = threading.Lock()

class LCDZeroMQ:
    def __init__(self, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:" + port)
        self.oled = sh1106(port=1, address=0x3C)
        self.font = ImageFont.load_default()
        self.font_ra = ImageFont.truetype('fonts/C&C Red Alert [INET].ttf', 10)
        self.deja_vu_sm = ImageFont.truetype('fonts/DejaVuSansCondensed.ttf', 10)
        self.deja_vu = ImageFont.truetype('fonts/DejaVuSansCondensed.ttf', 40)

    def go(self):
        while True:
            
            with lock:
               msgs = messages.copy()
            for k in msgs:
               _id = k
               msg = messages[k]
               self.do_draw(_id, msg)
               time.sleep(5000)  

           

    def do_draw(self, _id, msg):
        print(msg)
        tm = strftime("%H:%M:%S")

        if _id == "BME28":
            t,h,p = msg.split(":")
            with canvas(self.oled) as draw:
                draw.text((0, 0), "INDOOR - " + tm, font=self.deja_vu_sm, fill=255)
                draw.text((0, 10), t + "°C", font=self.deja_vu, fill=255)
                #draw.text((0, 20), h + "%", font=self.deja_vu, fill=255)
                draw.text((0, 50), p + "hPa " + h + "%", font=self.deja_vu_sm, fill=255)
        if _id == "CLOCK":
            t = msg
            with canvas(self.oled) as draw:
                draw.text((0, 10), t, font=self.deja_vu, fill=255)


e = LCDZeroMQ(sys.argv[1])

thread = Thread(target = e.go)
thread.start()

while True:
   message = e.socket.recv()
   message = message.decode('utf-8', 'ignore')
   _id = message[:5]
   msg = message[5:]

   with lock:
      messages[_id] = msg

   e.socket.send(b"\0")
print('End of lcd-zmq.py')
