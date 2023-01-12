import RPi.GPIO as GPIO
import time
import board
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

#oled display Imports
from pathlib import Path
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from PIL import ImageFont
font = ImageFont.load_default()
font_mc = ImageFont.truetype('/home/pi/Desktop/programs/MainMenu/Minecraft.ttf', 32)
font_mcsmall = ImageFont.truetype('/home/pi/Desktop/programs/MainMenu/Minecraft.ttf', 16)
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
x=0
top=0
width = device.width
height = device.height


#buttons
#7, 17, 9, 24
GPIO.setup(7, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(24, GPIO.IN)

menurun = 1
s = []


def matrixWithSwitch():
    global menurun
    global s
    
    
    def listToString(s):
        str1 = ""
        return(str1.join(s))
    
    while(menurun==1):
        
        with canvas(device) as draw:    
            draw.text((0, 1),  "Matrix Keypad"  ,  font=font_mcsmall, fill="white")
            draw.text((x +50, top+21),  ""  ,  font=font_mc, fill="white")
        with canvas(virtual) as draw:
            text(draw, (0, 0), str(listToString(s)), fill="white", font=proportional(LCD_FONT))
            
        #buttons    
            
        if GPIO.input(7):
            byte1 = 1
        else:
            byte1 = 0

        if GPIO.input(17):
            byte2 = 1
        else:
            byte2 = 0

        if GPIO.input(9):
            byte3 = 1
        else:
            byte3 = 0
            
        if GPIO.input(24):
            byte4 = 1
        else:
            byte4 = 0

        #button 1
        if(byte1==0 and byte2==0 and byte3==0 and byte4==1):
            print("Button 1 pressed")
            s.insert(0,'1')
            
            
        #button 2
        if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
            print("Button 2 pressed")
            s.insert(0,'2')
        #button 3
        if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
            print("Button 3 pressed")
            s.insert(0,'3')
        #button 4
        if(byte1==1 and byte2==1 and byte3==0 and byte4==1):
            print("Button 4 pressed")
            s.insert(0,'4')
        #button 5
        if(byte1==0 and byte2==0 and byte3==1 and byte4==1):
            print("Button 5 pressed")
            s.insert(0,'5')
        #button 6
        if(byte1==1 and byte2==0 and byte3==1 and byte4==1):
            print("Button 6 pressed")
            s.insert(0,'6')
            
        #button 7
        if(byte1==0 and byte2==1 and byte3==1 and byte4==1):
            print("Button 7 pressed")
            s.insert(0,'7')
        #button 8
        if(byte1==1 and byte2==1 and byte3==1 and byte4==1):
            print("Button 8 pressed")
            s.insert(0,'8')
matrixWithSwitch()




