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

#Relay setups
GPIO.setup(22,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
#enable active low
GPIO.output(22,GPIO.HIGH)
#relay numbers
RelayNum = 0

#buttons
#7, 17, 9, 24
GPIO.setup(7, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(24, GPIO.IN)

menurun = 1


def powerRelay():
    global menurun
    global RelayNum
    
    while(menurun==1):
        with canvas(device) as draw:
            draw.text((0, 1),  " Power Relay"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+21),  " Control"  ,  font=font_mcsmall, fill="white")
            if(RelayNum==1):
                draw.text((x, top+41),  " Relay 1: ON"  ,  font=font_mcsmall, fill="white")
            elif(RelayNum==2):
                draw.text((x, top+41),  " Relay 2: ON"  ,  font=font_mcsmall, fill="white")
            elif(RelayNum==3):
                draw.text((x, top+41),  " Relay 3: ON"  ,  font=font_mcsmall, fill="white")
            elif(RelayNum==4):
                draw.text((x, top+41),  " Relay 4: ON"  ,  font=font_mcsmall, fill="white")
            elif(RelayNum==0):
                draw.text((x, top+41),  " OFF"  ,  font=font_mcsmall, fill="white")
            

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
            print("Button 1 pressed")
            RelayNum=1
            
            
        #button 2
        if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
            print("Button 2 pressed")
            RelayNum=2
        #button 3
        if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
            print("Button 3 pressed")
            RelayNum=3
        #button 4
        if(byte1==1 and byte2==1 and byte3==0 and byte4==1):
            print("Button 4 pressed")
            RelayNum=4
        #button 5
        if(byte1==0 and byte2==0 and byte3==1 and byte4==1):
            print("Button 5 pressed")
            RelayNum=0
        #button 6
        if(byte1==1 and byte2==0 and byte3==1 and byte4==1):
            print("Button 6 pressed")
            menurun=0
            
        #button 7
        if(byte1==0 and byte2==1 and byte3==1 and byte4==1):
            print("Button 7 pressed")
            
        #button 8
        if(byte1==1 and byte2==1 and byte3==1 and byte4==1):
            print("Button 8 pressed")
            

        #relays process
            
        if(RelayNum==1):
            # #relay1
            GPIO.output(25,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
        elif(RelayNum==2):
            # #relay2
            GPIO.output(25,GPIO.HIGH)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
        elif(RelayNum==3):
            # #relay3
            GPIO.output(25,GPIO.LOW)
            GPIO.output(27,GPIO.HIGH)
            GPIO.output(22,GPIO.LOW)
        elif(RelayNum==4):
            #relay4
            GPIO.output(25,GPIO.HIGH)
            GPIO.output(27,GPIO.HIGH)
        else:
            GPIO.output(22,GPIO.HIGH)
powerRelay()
      