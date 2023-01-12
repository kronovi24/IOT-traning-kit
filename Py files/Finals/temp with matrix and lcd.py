import RPi.GPIO as GPIO
from time import sleep, strftime

#dotmatrix
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(5)
virtual = viewport(device, width=32, height=16)

import os
import glob

from pathlib import Path
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
import time
from PIL import ImageFont

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

font = ImageFont.load_default()
font_mc = ImageFont.truetype('/home/pi/Desktop/programs/MainMenu/Minecraft.ttf', 32)
font_mcsmall = ImageFont.truetype('/home/pi/Desktop/programs/MainMenu/Minecraft.ttf', 16)
x=0
top= 0


menurun = True


def temp():
    global menurun
    
    while menurun == True:
        
        if menurun == False:
            break
    
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
         
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
         
        def read_temp_raw():
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines
         
        def read_temp():
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f
        def read_tempC():
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c
            
        while True:
            with canvas(device) as draw:
                draw.text((x, top+2),  "Temperature Reading"  ,  font=font, fill=255)
                draw.text((x, top+20),  "Celsius & Farhanheit"  ,  font=font, fill=255)
                draw.text((x, top+40),  str(read_temp())  ,  font=font_mcsmall, fill=255)
            print(read_temp())
            with canvas(virtual) as draw:
                text(draw, (0, 0), str(read_tempC()), fill="white", font=proportional(LCD_FONT))
            
            
temp()    
