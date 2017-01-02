#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import sys
import threading
import zmq
import socket
import time
import pychromecast
from requests.utils import quote

from threading import Thread
from time import gmtime, strftime
from datetime import datetime

messages = {}
lock = threading.Lock()

import time
from pychromecast.controllers.media import MediaController
from pychromecast.controllers import BaseController

class MyController(MediaController):

    def __init__(self):
        super(MyController, self).__init__()

        self.url = ''
        self.cid = ''

    def receive_message(self, message, data):
        #print("Wow, I received this message: {}".format(data))
        
        info = data
        print(self)
        if 'type' in info and info['type'] == 'LOAD_CANCELLED':
            return super(MyController, self).receive_message(message, data)
        
        if 'status' in info and len(info['status']) == 0:
            print('Play default media.')
            self.play_media('http://192.240.102.133:12430/stream','audio/mp3')
            #time.sleep()
        else:            
            if info['type'] == 'MEDIA_STATUS':
                status = info['status'][0]                
                media = status['media']
                ct = media['contentType']
                url = media['contentId']
                print('------------> ',ct,url)
                if 'extendedStatus' in status:
                    extended_status = status['extendedStatus']['playerState']
                if 'playerStatus' in status:
                    extended_status = status['playerStatus']
                print('EXTENDED:', extended_status)
                if extended_status == 'LOADING':
                    print('Will store: ', url, ct)
                    print(url, ct)
                    if not 'google' in url and url != '':                            
                        self.url = url
                        self.cid = ct
                        print('SAVING', self.url)
                        # self.play_media(url, ct)
                        #
                
        return super(MyController, self).receive_message(message, data)


class Cast:
    def __init__(self, port):
        chromecasts = pychromecast.get_chromecasts()
        self.cast = next(cc for cc in chromecasts if cc.device.friendly_name == "AudioDongle")
        c = MyController()
        self.cast.register_handler(c)
        self.cast.wait()
        self.c = c
        #print(self.cast)
        print(self.c)
        
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:" + port)

    def go(self):
        while True:
            
            with lock:
               msgs = messages.copy()
            for k in msgs:
               _id = k
               msg = messages[k]
               print('Draw.')
               time.sleep(10)
               self.do_cast(_id, msg)               
               time.sleep(600)

           

    def do_cast(self, _id, msg):
        print(msg)
        tm = strftime("%H:%M:%S")

        if _id == "NRF24":
            t,h,p = msg.split(":")
            print(t,h,p)
            text = 'Temperatura je ' + t + ' stupnjeva. '
            text += 'Tlak zraka je ' + str(float(p.encode('ascii', 'ignore').strip('\x00'))) + ' hekto paskala. '
            text += 'Vlaznost je ' + h + ' posto. ' 
            text = quote(text)
            #mc = self.cast.media_controller
            self.c.update_status()
            time.sleep(20)
            print('self 1', self.c.url, self.c.cid)
            self.c.play_media('https://translate.google.com/translate_tts?ie=UTF-8&q=' + text + '&tl=hr&client=tw-ob', 'audio/mp3')
            time.sleep(30)
            print('self 2', self.c.url, self.c.cid)
            self.c.play_media(self.c.url, self.c.cid)

        if _id == "CLOCK":
            pass


e = Cast(sys.argv[1])

thread = Thread(target = e.go)
thread.start()

#messages['NRF24'] = "20:20:20"

while True:
   print('Waiting for message.')
   message = e.socket.recv()
   message = message.decode('utf-8', 'ignore')
   _id = message[:5]
   msg = message[5:]

   with lock:
      print(msg)
      messages[_id] = msg

   e.socket.send(b"\0")
print('End of lcd-zmq.py')
