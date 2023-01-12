import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#SERVOs
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

#buttons
#7, 17, 9, 24
GPIO.setup(7, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(24, GPIO.IN)


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
            
while True:
    servoRun()
            
