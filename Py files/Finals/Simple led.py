import RPi.GPIO as GPIO
import time
import board
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

# led strip
databit = 23
latch = 16
clock = 12
#order of bits 7,6,5,4,3,2,1,8
led1 = 0
led2 = 0
led3 = 0
led4 = 0
led5 = 0
led6 = 0
led7 = 0
led8 = 0
GPIO.setup(databit, GPIO.OUT)
GPIO.setup(latch, GPIO.OUT)
GPIO.setup(clock, GPIO.OUT)
#7, 17, 9, 24
GPIO.setup(7, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(24, GPIO.IN)
delay = 300
time.sleep(0.2)
GPIO.output(latch, 0)


menurun = 1

def ledDemo():
    global led1
    global led2
    global led3
    global led4 
    global led5 
    global led6 
    global led7 
    global led8
    
    global menurun
    
    GPIO.output(latch, 0)
        
    GPIO.output(databit, led8)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(databit, led7)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(databit, led6)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(databit, led5)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(databit, led4)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(databit, led3)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(databit, led2)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(databit, led1)
    GPIO.output(clock,1)
    GPIO.output(clock,0)

    GPIO.output(latch,1)
        
    
    while(menurun==1):
        with canvas(device) as draw:    
            
            draw.text((x, top+21), "8 Leds" ,  font=font_mc, fill="white")
        
        while(1):
            for y in range(8):
                GPIO.output(databit, 1)
                GPIO.output(clock,1)
                GPIO.output(clock,0)
                GPIO.output(latch,1)
                time.sleep(0.2)
                GPIO.output(latch,0)
            
            for y in range(8):
                GPIO.output(databit, 0)
                GPIO.output(clock,1)
                GPIO.output(clock,0)
                GPIO.output(latch,1)
                time.sleep(0.2)
                GPIO.output(latch,0)
ledDemo()
       
    