#!/usr/bin/python3

import dbus
import dbus.service
import sys
from gi.repository import GObject
import dbus.mainloop.glib
import threading

from i2clibraries import i2c_lcd
import time
# Configuration parameters
# I2C Address, Port, Enable pin, RW pin, RS pin, Data 4 pin, Data 5 pin, Data 6 pin, Data 7 pin, Backlight pin (optional)
lcd = i2c_lcd.i2c_lcd(0x20, 1, 4, 5, 6, 0, 1, 2, 3, 7)
# If you want to disable the cursor, uncomment the following line
lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)

NUM_CHARS=32
NUM_CHARS_IN_ROW=16
ROLL_NUM=2

maps = {}

class LCDDBus(dbus.service.Object):
    def __init__(self, maps):
        """
            claim dbus service
        """
        self.maps = maps
        bus_name = dbus.service.BusName('com.svesoftware.raspberry.lcd', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/com/svesoftware/raspberry/lcd')

        self.l = LCD(maps)
        self.l.set_lcd(lcd)
	


    @dbus.service.method('com.svesoftware.raspberry.lcd', in_signature='sss', out_signature='s')
    def draw(self, text, sender, mode):
        print('Sender, mode:', sender, mode)
        start_time = time.time()
        self.maps[sender] = text
        print(len(self.maps))
        self.l.go()
        return 'ok'


class LCD():
    def __init__(self, maps):
        self.maps = maps

    def set_lcd(self, lcd):
        self.lcd = lcd

    def init_lcd(self):
        """
            initialize and clean lcd screen
        """
        self.lcd.clear()
        self.lcd.home()
        self.lcd.backLightOff()
        self.lcd.setPosition(1, 0)
        
    def _display_page(self, text):
        self.lcd.setPosition(1,0)
        self.lcd.writeString(text[:NUM_CHARS_IN_ROW])
        self.lcd.setPosition(2,0)
        self.lcd.writeString(text[NUM_CHARS_IN_ROW:])
        
    def _wait_some_more(self):
        time.sleep(5)
    
    def _wait_some(self):
        time.sleep(1)

    def go(self):
        print('Go')
        try:
           t = threading.Thread(target=self.display)
           #t.setDaemon(True)
           #print(t.daemon)
           t.start()
           t.join()
        except Exception as inst:
           print('Error')
           return "error:" + str(inst)
        print('Out of go')
    
    def display(self):
        print('Start thread')
        #print('Received: ', text)
        p = 0
        while p < 1:
           p = p + 1
           print('doing it..')
           self.init_lcd()
           print('then...')
           for key in self.maps:
              print('what?')
              text = self.maps[key]
              print('Show text', text)
        
              if len(text) > NUM_CHARS:
                 # 'text' is bigger than total number of characters on a screen.
                 # we are going to roll text page by page for ROLL_NUM number of times           
                 for roll in range(ROLL_NUM):
              
                    # display initial text (first page)
                    self._display_page(text[:NUM_CHARS])
                    self._wait_some()
           
                    # display rest of the pages
                    for i in range(NUM_CHARS, len(text), NUM_CHARS):
                 
                       end = False
                       # display first row
                       self.lcd.setPosition(1,0)                 
                       s = i + NUM_CHARS_IN_ROW
                       if len(text) < s:
                          s = len(text)
                          end = True
                       self.lcd.writeString(text[i:s].ljust(NUM_CHARS_IN_ROW))
                 
                       if not end:
                          # display second row
                          self.lcd.setPosition(2,0)
                          if len(text) < NUM_CHARS_IN_ROW + s:
                              self.lcd.writeString(text[s:].ljust(NUM_CHARS_IN_ROW))
                          else:
                              self.lcd.writeString(text[s:s + NUM_CHARS_IN_ROW].ljust(NUM_CHARS_IN_ROW))

                       self._wait_some()
       
              else:
                 self._display_page(text)
                 self._wait_some_more()   

        print('Exiting')

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
loop = GObject.MainLoop()
e = LCDDBus(maps)

loop.run()

print('end')
