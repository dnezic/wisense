# wisense

Home wireless weather station for Raspberry Pi and ATTINY.

## Basic informations

Project is based on Raspberry Pi which acts as a message receiver for remote wireless sensors.
Wireless communication is based on nRF24L01P+ chip from Nordic Semiconductor, and Raspberry Pi libraries are borrowed from [https://github.com/stanleyseow/RF24](https://github.com/stanleyseow/RF24).

Source code for remote wireless weather station can be found here: [https://github.com/dnezic/wisense-avr](https://github.com/dnezic/wisense-avr)

## Project installation

*Note: we are starting from raspbian minimal image*

Execute `raspi-config`, setup under *Advanced options*:

* enable SPI
* enable I2C
* disable serial console

Make dir `git` in home folder.

Install git: `sudo apt-get install git`

And then clone into folder `git`:
```bash
~/git> git clone https://github.com/dnezic/wisense.git
~/git> cd wisense
```

Install pip3 and python3:
```bash
sudo apt-get install python3-pip
sudo apt-get install python3
```

Install additional dependencies:
```bash
sudo apt-get install python3-zmq
sudo apt-get install python3-smbus
sudo apt-get install python3-pil
```

## LCD
LCD service simply listens to incoming ZMQ messages. Register LCD service:
```bash
sudo cp ~/git/wisense/docs/systemd/lcd-zmq.service /etc/systemd/system/
sudo systemctl enable lcd-zmq
sudo systemctl daemon-reload
sudo systemctl start lcd-zmq
```

Test LCD service:
```bash
cd /home/pi/git/wisense/lcd-ssd1306
sudo python3 lcd-send-time.py 6000
```

Set crontab:
```bash
crontab -e
* * * * * /home/pi/git/wisense/lcd-ssd1306/lcd-send-time.py 6000
```

If something is wrong, check if 0x3c (LCD) is visible:
```bash
sudo i2cdetect -y 1
```

Disable CRON logging:
```bash
sudo vi /etc/default/cron
EXTRA_OPTS="-L 0"

sudo service cron restart
```

## BME 280
BME 280 is connected via I2C.
Add to crontab:
```bash
* * * * * sudo python3 /home/pi/git/wisense/bme280/bme280.py 6000
```

## nrf24
nRF24L01P is connected via SPI.

```bash
sudo apt-get install libzmq-dev

# into same folder 'git'
cd ~/git
~/git> git clone https://github.com/stanleyseow/RF24.git
~/git> cd RF24/RPi/RF24
make
sudo make install
```
This will install RF24 libraries and headers to /usr/local/(include|lib)

```bash
cd ~/git/wisense/rf24sense-zmq/
make
sudo make install
```

Register systemd service:
```bash
sudo cp ~/git/wisense/docs/systemd/rf24-zmq.service /etc/systemd/system/
sudo systemctl enable rf24-zmq
sudo systemctl daemon-reload
sudo systemctl start rf24-zmq
```

Customize lcd-zmq.py with various fonts or display variations.
