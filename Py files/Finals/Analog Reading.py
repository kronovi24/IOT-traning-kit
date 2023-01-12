import RPi.GPIO as GPIO
import busio
import board
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


menurun = 1

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
                   
analogreaders()