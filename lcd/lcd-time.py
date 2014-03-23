#run command: sudo python3 lcd_time.py
import sys
sys.path.append('/quick2wire/')
from i2clibraries import i2c_lcd
import time
from subprocess import * 
from datetime import datetime

# Configuration parameters
# I2C Address, Port, Enable pin, RW pin, RS pin, Data 4 pin, Data 5 pin, Data 6 pin, Data 7 pin, Backlight pin (optional)
lcd = i2c_lcd.i2c_lcd(0x20, 1, 4, 5, 6, 0, 1, 2, 3, 7)

# If you want to disable the cursor, uncomment the following line
lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)

cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	output = output.decode("utf-8").rstrip()
	return output

while 1:	
	lcd.setPosition(1, 0)
	lcd.writeString(datetime.now().strftime('%b %d %H:%M:%S\n').rstrip())
	lcd.setPosition(2, 0)
	ipaddr = run_cmd(cmd)	
	lcd.writeString('IP %s' % ( ipaddr ) )
	time.sleep(0.5)

