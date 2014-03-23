#run command: sudo python3 lcd_off.py
import sys
sys.path.append('/quick2wire/')
from i2clibraries import i2c_lcd

# Configuration parameters
# I2C Address, Port, Enable pin, RW pin, RS pin, Data 4 pin, Data 5 pin, Data 6 pin, Data 7 pin, Backlight pin (optional)
lcd = i2c_lcd.i2c_lcd(0x20, 1, 4, 5, 6, 0, 1, 2, 3, 7)

lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)
lcd.clear()
lcd.backLightOff()
