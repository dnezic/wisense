wisense
=======

Home wireless weather station for Raspberry Pi and ATTINY.

Basic informations
------------------

Project is based on Raspberry Pi which acts as a message receiver for remote wireless sensors.
Wireless communication is based on nRF24L01P+ chip from Nordic Semiconductor, and Raspberry Pi libraries are borrowed from [https://github.com/stanleyseow/RF24](https://github.com/stanleyseow/RF24) and maybe little cleaned up.

Project list
------------------

### 1. lcd
Folder **lcd** contains python code for communication with LCD 16x02 display using I2C protocol. I2C is enabled using **mjkdz** board in order to save a lot of GPIO pins.
Python script **lcd-dbus.py** listens for incoming dbus messages and sends them to the LCD display.
Configuration for dbus protocol is placed in *docs/dbus-configuration* folder. Folder tree needs to be copied over Raspberry Pi filesystem but before that, the file **com.svesoftware.raspberry.lcd.service** in folder */docs/dbus-configuration/usr/share/dbus-1/system-services* has to be modified to match exact path of **lcd-dbus.py** script. This is required for dbus to automatically starts script when specific message is received by dbus service.

####Test LCD screen:
```bash
#> python3 lcd-send.py
```
or
```bash
#> python3 lcd-time.py
```


### 2. rf24sense-dbus
It receives messages from nRF24L01P+ chip and sends them to the lcd using dbus protocol.
Transmission is set to "No acknowledge" with fixed payload length in order to achieve longer distances.

####Prerequisites:
* dbus-sender

  A
* rf4l

  B

