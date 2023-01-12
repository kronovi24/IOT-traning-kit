
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

#buttons
#7, 17, 9, 24
GPIO.setup(7, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(24, GPIO.IN)

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

def ledstrip():
    global led1
    global led2
    global led3
    global led4 
    global led5 
    global led6 
    global led7 
    global led8
    
    global menurun
    
    def register():
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

    register()

    while(menurun==1):
        
        with canvas(device) as draw:    
            draw.text((0, 1),  "8-bits"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+21), str(led1) + str(led2) + str(led3) + str(led4) + str(led5) + str(led6) + str(led7) + str(led8) ,  font=font_mc, fill="white")
        

        
        #buttons
        
        #button decoder
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
            

        #print(byte1, byte2,byte3,byte4)
        #time.sleep(0.5)

        #button 1
        if(byte1==0 and byte2==0 and byte3==0 and byte4==1):
            if(led1==1  ):
                led1 = 0
                time.sleep(0.2)
            elif(led1==0  ):
                led1 = 1
                time.sleep(0.2)
            register()
        #button 2
        if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
            if(led2==1  ):
                led2 = 0
                time.sleep(0.2)
            elif(led2==0  ):
                led2 = 1
                time.sleep(0.2)
            register()
        #button 3
        if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
            if(led3==1  ):
                led3 = 0
                time.sleep(0.2)
            elif(led3==0  ):
                led3 = 1
                time.sleep(0.2)
            register()
        #button 4
        if(byte1==1 and byte2==1 and byte3==0 and byte4==1):
            if(led4==1  ):
                led4 = 0
                time.sleep(0.2)
            elif(led4==0  ):
                led4 = 1
                time.sleep(0.2)
            register()
        #button 5
        if(byte1==0 and byte2==0 and byte3==1 and byte4==1):
            if(led5==1  ):
                led5 = 0
                time.sleep(0.2)
            elif(led5==0  ):
                led5 = 1
                time.sleep(0.2)
            register()
        #button 6
        if(byte1==1 and byte2==0 and byte3==1 and byte4==1):
            if(led6==1  ):
                led6 = 0
                time.sleep(0.2)
            elif(led6==0  ):
                led6 = 1
                time.sleep(0.2)
            register()
        #button 7
        if(byte1==0 and byte2==1 and byte3==1 and byte4==1):
            if(led7==1  ):
                led7 = 0
                time.sleep(0.2)
            elif(led7==0  ):
                led7 = 1
                time.sleep(0.2)
            register()
        #button 8
        if(byte1==1 and byte2==1 and byte3==1 and byte4==1):
            if(led8==1  ):
                led8 = 0
                time.sleep(0.2)
            elif(led8==0  ):
                led8 = 1
                time.sleep(0.2)
            register()
    
ledstrip()