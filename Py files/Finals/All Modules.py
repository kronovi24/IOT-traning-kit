import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#onewire
import os
import glob


#7segments
import busio
import board
import busio
from adafruit_ht16k33 import segments

#Dot matrix
import argparse
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(5)
virtual = viewport(device, width=32, height=16)

y = []

#matrix keypad
import digitalio
import adafruit_matrixkeypad
cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D5, board.D26)]
rows = [digitalio.DigitalInOut(x) for x in (board.D6, board.D21, board.D20, board.D19)]
keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
sample = 0
spacing = 20
s = []
#7 segments setups
from time import strftime
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)
# Clear the display.
display.fill(0)

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

#SERVOs
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)


#menu variables
selectorchoice = 1
menupage = 1
menurun = 0

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



def menu():
    global selectorchoice
    global menupage
    global menurun
    
    with canvas(device) as draw:
        if selectorchoice == 1:
            draw.rectangle((0,0,width-1,15), outline=1, fill=0)
        if selectorchoice == 2:
            draw.rectangle((0,top+19,width-1,40), outline=1, fill=0)
        if selectorchoice == 3:
            draw.rectangle((0,top+39,width-1,58), outline=1, fill=0)
        if(menupage==1):
            draw.text((0, 1),  " 7-Segments"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+21),  " Analog Reader"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+41),  " Matrix Keypad"  ,  font=font_mcsmall, fill="white")
        if(menupage==2):
            draw.text((0, 1),  "Power Relay"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+21),  "Dot Matrix"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+41),  "led Switch"  ,  font=font_mcsmall, fill="white")
        
        if(menupage==3):
            draw.text((0, 1),  "Led Demo"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+21),  "Dot Switch"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+41),  "Servo Control"  ,  font=font_mcsmall, fill="white")
        if(menupage==4):
            draw.text((0, 1),  "read Temp"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+21),  ">Blank<"  ,  font=font_mcsmall, fill="white")
            draw.text((x, top+41),  ">Blank<"  ,  font=font_mcsmall, fill="white")
        
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
        if(selectorchoice>0):
            selectorchoice = selectorchoice - 1
            if(selectorchoice==0):
                selectorchoice = 3
                menupage = menupage - 1
            if(menupage == 0):
                menupage = 4
                selectorchoice = 3
        
        time.sleep(0.2)
        
    #button 2
    if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
        print("Button 2 pressed")
        if(selectorchoice<5):
            selectorchoice = selectorchoice + 1
        if(selectorchoice==4):
            selectorchoice = 1
            if(menupage<4):
                menupage = menupage +1
            else:
                menupage = 1
        time.sleep(0.2)
        
    #button 3
    if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
        print("Button 3 pressed")
        menurun = 1
        time.sleep(0.2)

def segment():
    global menurun
    while(menurun==1):
        with canvas(device) as draw:
            draw.text((x, top+30),  "<Display Time>"  ,  font=font_mcsmall, fill=255)
               
        display.print(strftime("%I:%M"))
        
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

def analogreaders():
    global menurun
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)
    # you can specify an I2C adress instead of the default 0x48
    # ads = ADS.ADS1115(i2c, address=0x49)    
    chan = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    chan2 = AnalogIn(ads, ADS.P2)
    chan3 = AnalogIn(ads, ADS.P3)
    # Create differential input between channel 0 and 1
    # chan = AnalogIn(ads, ADS.P0, ADS.P1)
    
    
    while(menurun==1):
        with canvas(device) as draw:
            draw.text((x+40, top+2),  "Raw"  ,  font=font, fill=255)
            draw.text((x+80, top+2),  "Voltage"  ,  font=font, fill=255)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x+40, top),  "Raw"  ,  font=font, fill=255)
            draw.text((x+80, top),  "Voltage"  ,  font=font, fill=255)

            #analog 0
            draw.text((x+15, top+10),  "A0" ,  font=font, fill=255)
            draw.text((x+40, top+10),  str(chan.value) ,  font=font, fill=255)
            draw.text((x+80, top+10),  str(chan.voltage) ,  font=font, fill=255)
            
            #analog1
            draw.text((x+15, top+20),  "A1",  font=font, fill=255)
            draw.text((x+40, top+20),  str(chan1.value) ,  font=font, fill=255)
            draw.text((x+80, top+20),  str(chan1.voltage) ,  font=font, fill=255)
            
            #analog2
            draw.text((x+15, top+30),  "A2",  font=font, fill=255)
            draw.text((x+40, top+30),  str(chan2.value) ,  font=font, fill=255)
            draw.text((x+80, top+30),  str(chan2.voltage) ,  font=font, fill=255)
            
            #analog3
            draw.text((x+15, top+40),  "A3",  font=font, fill=255)
            draw.text((x+40, top+40),  str(chan3.value) ,  font=font, fill=255)
            draw.text((x+80, top+40),  str(chan3.voltage) ,  font=font, fill=255)
            
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
        if(led1==1 and led2==1 and led3==1 and led4==1 and led5==1 and led6==1 and led7==1 and led8==1):
            menurun = 0
            led1 = 0
            led2 = 0
            led3 = 0
            led4 = 0
            led5 = 0
            led6 = 0
            led7 = 0
            led8 = 0
            register()

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
        
        menurun=0

def DotMatrix():
    global menurun
    
    with canvas(device) as draw:    
        draw.text((x + 10, 1),  "Dot Matrix "  ,  font=font_mcsmall, fill="white")
        draw.text((x + 1, top+21), "Sample Diplay"  ,  font=font_mcsmall, fill="white")
    
    
    while(menurun==1):
        def output(n, block_orientation, rotate, inreverse, text):
            # create matrix device
            serial = spi(port=0, device=0, gpio=noop())
            device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                             rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
            print(text)

            show_message(device, text, fill="white", font=proportional(CP437_FONT), scroll_delay=0.05)
            time.sleep(1)


        if __name__ == "__main__":
            parser = argparse.ArgumentParser(description='view_message arguments',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

            parser.add_argument('--cascaded', '-n', type=int, default=4, help='Number of cascaded MAX7219 LED matrices')
            parser.add_argument('--block-orientation', type=int, default=-90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
            parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
            parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')
            parser.add_argument('--text', '-t', default='>>HELLO WORLD', help='Set text message')
            args = parser.parse_args()

        try:
            output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, args.text)
            menurun = 0
        except KeyboardInterrupt:
            pass

def DotSwitch():
    global menurun
    global y
    
    
    def listToString(y):
        str1 = ""
        return(str1.join(y))
    
    while(menurun==1):
        
        with canvas(device) as draw:    
            draw.text((0, 1),  "Matrix Keypad"  ,  font=font_mcsmall, fill="white")
            draw.text((x +50, top+21),  ""  ,  font=font_mc, fill="white")
        with canvas(virtual) as draw:
            text(draw, (0, 0), str(listToString(y)), fill="white", font=proportional(LCD_FONT))
            
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
            y.insert(0,'1')
            
            
        #button 2
        if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
            print("Button 2 pressed")
            y.insert(0,'2')
        #button 3
        if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
            print("Button 3 pressed")
            y.insert(0,'3')
        #button 4
        if(byte1==1 and byte2==1 and byte3==0 and byte4==1):
            print("Button 4 pressed")
            y.insert(0,'4')
        #button 5
        if(byte1==0 and byte2==0 and byte3==1 and byte4==1):
            print("Button 5 pressed")
            y.insert(0,'5')
        #button 6
        if(byte1==1 and byte2==0 and byte3==1 and byte4==1):
            print("Button 6 pressed")
            y.insert(0,'6')
            
        #button 7
        if(byte1==0 and byte2==1 and byte3==1 and byte4==1):
            print("Button 7 pressed")
            y.insert(0,'7')
        #button 8
        if(byte1==1 and byte2==1 and byte3==1 and byte4==1):
            print("Button 8 pressed")
            with canvas(virtual) as draw:
                text(draw, (0, 0), "", fill="white", font=proportional(LCD_FONT))
          
            menurun = 0
def servoRun():
    global menurun
    a = '\u00b0'
    servoselector = 1
    
    p1 = GPIO.PWM(13, 50)
    p1.start(0)
    rot1 = 0
    angle1 = 0
    
    p2 = GPIO.PWM(12,50)
    p2.start(0)
    rot2 = 0
    angle2 = 0
    
    angleall = 0
    
    p3 = GPIO.PWM(19,50)
    p3.start(0)
    rot3 = 0
    angle3 =0
    degree_sign= u'\N{DEGREE SIGN}'
    
    while menurun == 1:
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
            if servoselector <4:
                servoselector = servoselector +1
                time.sleep(0.3)
            else:
                servoselector = 1
                time.sleep(0.3)
        
            
        
           
        #button 5
        if(byte1==0 and byte2==0 and byte3==1 and byte4==1):
            print("Button 5 pressed")
            
        #button 6
        if(byte1==1 and byte2==0 and byte3==1 and byte4==1):
            print("Button 6 pressed")
            
            
        #button 7
        if(byte1==0 and byte2==1 and byte3==1 and byte4==1):
            print("Button 7 pressed")
            
        #button 8
        if(byte1==1 and byte2==1 and byte3==1 and byte4==1):
            print("Button 8 pressed")
            
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            if servoselector == 1:
                draw.text((x+5, top+5),  "Servo 1 online"  ,  font=font_mcsmall, fill=255)
                draw.text((x+5, top+20),  "Angle:"   ,  font=font_mcsmall, fill=255)
                draw.text((x+60, top+20),  str(angle1)  ,  font=font_mcsmall, fill=255)
                if angle1 == 0 :
                    draw.text((x+50, top+50),  "Min"   ,  font=font_mcsmall, fill=255)
                if angle1 == 180 :
                    draw.text((x+50, top+50),  "Max"   ,  font=font_mcsmall, fill=255)
            if servoselector == 2:
                draw.text((x+5, top+5),  "Servo 2 online"  ,  font=font_mcsmall, fill=255)
                draw.text((x+5, top+20),  "Angle:"   ,  font=font_mcsmall, fill=255)
                draw.text((x+60, top+20),  str(angle2)  ,  font=font_mcsmall, fill=255)
                if angle2 == 0 :
                    draw.text((x+50, top+50),  "Min"   ,  font=font_mcsmall, fill=255)
                if angle2 == 180 :
                    draw.text((x+50, top+50),  "Max"   ,  font=font_mcsmall, fill=255)
                
            if servoselector == 3:
                draw.text((x+5, top+5),  "Servo 3 online"  ,  font=font_mcsmall, fill=255)
                draw.text((x+5, top+20),  "Angle:"   ,  font=font_mcsmall, fill=255)
                draw.text((x+60, top+20),  str(angle3)  ,  font=font_mcsmall, fill=255)
                if angle3 == 0 :
                    draw.text((x+50, top+50),  "Min"   ,  font=font_mcsmall, fill=255)
                if angle3 == 180 :
                    draw.text((x+50, top+50),  "Max"   ,  font=font_mcsmall, fill=255)
            if servoselector == 4:
                draw.text((x+5, top+5),  "All servo online"  ,  font=font_mcsmall, fill=255)
                draw.text((x+5, top+20),  "Angle:"   ,  font=font_mcsmall, fill=255)
                draw.text((x+60, top+20),  str(angleall)  ,  font=font_mcsmall, fill=255)
                if angleall == 0 :
                    draw.text((x+50, top+50),  "Min"   ,  font=font_mcsmall, fill=255)
                if angleall == 180 :
                    draw.text((x+50, top+50),  "Max"   ,  font=font_mcsmall, fill=255)   
       
        
        if servoselector ==1:
            if rot1==0:
                p1.ChangeDutyCycle(2)
                angle1= 0
            if rot1==1:
                p1.ChangeDutyCycle(4)
                angle1 = 45
            if rot1==2:
                p1.ChangeDutyCycle(7)
                angle1 = 90
            if rot1==3:
                p1.ChangeDutyCycle(9.5)
                angle1 = 135
            if rot1==4:
                p1.ChangeDutyCycle(12)
                angle1= 180
              
            #button 2
            if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
                print("Button 2 pressed")
                if rot1>0:
                    rot1=rot1-1
                    print(rot1)
                    time.sleep(0.3)
            
            #button 3
            if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
                print("Button 3 pressed")
                if rot1<4:
                    rot1=rot1+1
                    print(rot1)
                    time.sleep(0.3)
            
        
        if servoselector == 2:
            if rot2==0:
                p2.ChangeDutyCycle(2)
                angle2 = 0
            if rot2==1:
                p2.ChangeDutyCycle(4)
                angle2 = 45
            if rot2==2:
                p2.ChangeDutyCycle(7)
                angle2 = 90
            if rot2==3:
                p2.ChangeDutyCycle(9.5)
                angle2 = 135
            if rot2==4:
                p2.ChangeDutyCycle(12)
                angle2 = 180
            
                    #button 2
            if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
                print("Button 2 pressed")
                if rot2>0:
                    rot2=rot2-1
                    print(rot2)
                    time.sleep(0.3)
            
            #button 3
            if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
                print("Button 3 pressed")
                if rot2<4:
                    rot2=rot2+1
                    print(rot2)
                    time.sleep(0.3)
            
        
        if servoselector ==3:
            if rot3==0:
                p3.ChangeDutyCycle(2)
                angle3 = 0
            if rot3==1:
                p3.ChangeDutyCycle(4)
                angle3 = 45
            if rot3==2:
                p3.ChangeDutyCycle(7)
                angle3 = 90
            if rot3==3:
                p3.ChangeDutyCycle(9.5)
                angle3 = 135
            if rot3==4:
                p3.ChangeDutyCycle(12)
                angle3 = 180
            
            #button 2
            if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
                print("Button 2 pressed")
                if rot3>0:
                    rot3=rot3-1
                    print(rot3)
                    time.sleep(0.3)
            
            #button 3
            if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
                print("Button 3 pressed")
                if rot3<4:
                    rot3=rot3+1
                    print(rot3)
                    time.sleep(0.3)
            
        
                   
        if servoselector == 4:
            if rot2==0:
                p3.ChangeDutyCycle(2)
                p2.ChangeDutyCycle(2)
                p1.ChangeDutyCycle(2)
                angleall = 0
            if rot2==1:
                p3.ChangeDutyCycle(4)
                p2.ChangeDutyCycle(4)
                p1.ChangeDutyCycle(4)
                angleall = 45
            if rot2==2:
                p3.ChangeDutyCycle(7)
                p2.ChangeDutyCycle(7)
                p1.ChangeDutyCycle(7)
                angleall = 90
            if rot2==3:
                p3.ChangeDutyCycle(9.5)
                p2.ChangeDutyCycle(9.5)
                p1.ChangeDutyCycle(9.5)
                angleall = 135
            if rot2==4:
                p3.ChangeDutyCycle(12)
                p2.ChangeDutyCycle(12)
                p1.ChangeDutyCycle(12)
                angleall = 180
            
            #button 2
            if(byte1==1 and byte2==0 and byte3==0 and byte4==1):
                print("Button 2 pressed")
                if rot2>0:
                    rot2=rot2-1
                    print(rot2)
                    time.sleep(0.3)
            
            #button 3
            if(byte1==0 and byte2==1 and byte3==0 and byte4==1):
                print("Button 3 pressed")
                if rot2<4:
                    rot2=rot2+1
                    print(rot2)
                    time.sleep(0.3)
            
                
        if menurun == 0:
            break
        
            
        #button 4
        if(byte1==1 and byte2==1 and byte3==0 and byte4==1):
            print("Button 4 pressed")
            print("exit success")
            menurun = 0
def temp():
    global menurun
    
    while menurun == 1:
        
        if menurun == 0:
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
            
        while(menurun==1):
            with canvas(device) as draw:
                draw.text((x, top+2),  "Temperature Reading"  ,  font=font, fill=255)
                draw.text((x, top+20),  "Celsius & Farhanheit"  ,  font=font, fill=255)
                draw.text((x, top+40),  str(read_temp())  ,  font=font_mcsmall, fill=255)
            print(read_temp())
            with canvas(virtual) as draw:
                text(draw, (0, 0), str(read_tempC()), fill="white", font=proportional(LCD_FONT))
            
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
                menurun = 0
            

try:    
    while(1):
        while(menurun==0):
            menu()
        
        #7 segment i2c device
        if(selectorchoice==1 and menupage==1 and menurun==1):
            segment()
        #ads analog reader i2c
        if(selectorchoice==2 and menupage==1 and menurun==1):
            analogreaders()
        #Matrix keypad
        if(selectorchoice==3 and menupage==1 and menurun==1):
            matrixKeypad()
        #power relay
        if(selectorchoice==1 and menupage==2 and menurun==1):
            powerRelay()
         #Dotmatrix
        if(selectorchoice==2 and menupage==2 and menurun==1):
            DotMatrix()
        #ledstrip
        if(selectorchoice==3 and menupage==2 and menurun==1):
            ledstrip()
            
        if(selectorchoice==1 and menupage==3 and menurun==1):
            ledDemo()
        if(selectorchoice==2 and menupage==3 and menurun==1):
            DotSwitch()
        if(selectorchoice==3 and menupage==3 and menurun==1):
            servoRun()
        if(selectorchoice==1 and menupage==4 and menurun==1):
            temp()
        

  
finally:  
    GPIO.cleanup() # this ensures a clean exit  