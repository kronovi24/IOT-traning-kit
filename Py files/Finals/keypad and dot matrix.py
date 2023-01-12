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


#matrix keypad
import digitalio
import adafruit_matrixkeypad
cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D5, board.D26)]
rows = [digitalio.DigitalInOut(x) for x in (board.D6, board.D21, board.D20, board.D19)]
keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
sample = 0
spacing = 20

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


#7segments
import busio
import board
import busio
from adafruit_ht16k33 import segments

#7 segments setups
from time import strftime
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)
# Clear the display.
display.fill(0)


#buttons
#7, 17, 9, 24
GPIO.setup(7, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(24, GPIO.IN)

menurun = 1
s = []


def matrixKeypad():
    global menurun
    global sample
    global spacing
    global s
    
    def listToString(s):
        str1= ""
        return(str1.join(s))
    
    
    while(menurun==1):
        #keypad logic
        keys = keypad.pressed_keys
        if keys:
            if(keys==[1]):
                sample = 1
                s.insert(0,'1')
            if(keys==[2]):
                sample = 2
                s.insert(0,'2')
            if(keys==[3]):
                sample = 3
                s.insert(0,'3')
            if(keys==[4]):
                sample = 4
                s.insert(0,'4')
            if(keys==[5]):
                sample = 4
                s.insert(0,'5')
            if(keys==[6]):
                sample = 6
                s.insert(0,'6')
            if(keys==[7]):
                sample = 7
                s.insert(0,'7')
            if(keys==[8]):
                sample = 8
                s.insert(0,'8')
            if(keys==[9]):
                sample = 9
                s.insert(0,'9')
            if(keys==[0]):
                sample = 0
                s.insert(0,'0') 
            if(keys==["*"]):
                sample = "*"
                s.insert(0,'*')
            if(keys==["#"]):
                sample = "#"
                s.insert(0,'#')
            display.print(sample)
            time.sleep(0.2)
            
        with canvas(device) as draw:    
            draw.text((0, 1),  "Matrix Keypad"  ,  font=font_mcsmall, fill="white")
            draw.text((x +50, top+21),  str(sample)  ,  font=font_mc, fill="white")
        with canvas(virtual) as draw:
            text(draw, (0, 0), str(listToString(s)), fill="white", font=proportional(LCD_FONT))
            
        
        
        #buttons
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
        #button 3
        if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
            print("Button 3 pressed")
            menurun = 0
            time.sleep(0.2)    

matrixKeypad()



