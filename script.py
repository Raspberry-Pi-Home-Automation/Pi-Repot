#!/usr/bin/python
# Main structure of script created by Toshi Bass
# Python 3.2 Raspbian (Wheezy) V7

# Imports
import webiopi
import json
import sys
import time
import datetime
import os
import subprocess
import Adafruit_DHT  #import the Adafruit module
 


sys.path.append("/home/pi/project/html") # Point to the doc folder

# Enable debug output
webiopi.setDebug()
from webiopi.utils.logger import info

# Retrieve GPIO lib
GPIO = webiopi.GPIO

##################################################################
# Import Connected Devices (Only devices supported by webiopi)
##################################################################



##################################################################
# Called by WebIOPi at script loading
##################################################################

##Sensor and Pin used by DHT11 humidity and temperature sensor
sensor = Adafruit_DHT.DHT11
pin = '4'
#Led pin
LED1 = 23
#Light Sensor Pin
LsrPin = 25
#Motion Sensor Pin
PIR_PIN= 12
#Buzzer Pin
Buzz = 16
ledder="off" #just for testing

def setup():
    webiopi.debug("Script with macros - Setup")
    # Setup GPIOs
    GPIO.setFunction(LED1, GPIO.OUT)
    GPIO.setFunction(PIR_PIN, GPIO.IN)
    GPIO.setFunction(Buzz, GPIO.OUT)
    os.system("sudo service motion start")

##################################################################
#Setup Vars
##################################################################

i0,i1,i2,i3,i4,i5,i6,i7,i8,i9 = 0,0,0,0,0,0,0,0,0,0


##################################################################
# Define Functions
##################################################################

#           Function for Photorresistor                          #
# Counts how long it takes for the capacitor to charge           #
# In bright light capacitor charges very quick = low values      #
# In darkness the capacitor takes longer to charge = high values #  
def rc_time(LsrPin):
 count=0
 GPIO.setup(LsrPin, GPIO.OUT)
 GPIO.output(LsrPin, GPIO.LOW)
 time.sleep(1)
 GPIO.setup(LsrPin, GPIO.IN)
 while(GPIO.input(LsrPin)==GPIO.LOW):
  count +=0.01
 return count

#          Function for Temperature and Humidity                    #
#   Calls an Adafruit function taking in the sensor and pin         #

def get_temp():
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   h=str(humidity ) + "%"
   t=str(temperature ) + "*C"
   return h, t

#           Function to get the MOTION DETECTED status                #
#        Returns the status stating if  movement was detected #
def get_movement_status():
   if (GPIO.digitalRead(PIR_PIN)==GPIO.HIGH):
       move="Movement Detected" 
   elif (GPIO.digitalRead(PIR_PIN)==GPIO.LOW):   
       move="No movement detected"
   return  move


 
##################################################################
# Looped by WebIOPi
##################################################################

def loop():
    GPIO.digitalWrite(Buzz, GPIO.LOW)
    buzzTest="NO Buzz" # for debugging
    #Set a variable to the count returned by the sensor function
    countValue= rc_time(LsrPin)
    # use the value of the count to set led pin to high(on) or low(off)
    #Led also turns on if motion detected
    if(countValue>100 or  GPIO.digitalRead(PIR_PIN)==GPIO.HIGH):
        GPIO.digitalWrite(LED1, GPIO.HIGH)
#        os.system("sudo fswebcam ServerTest.jpg")
      #  os.system("./webcam.sh")

        ledder="Motion Detected and Led On" # for debugging only
    else:
        GPIO.digitalWrite(LED1,GPIO.LOW)
        ledder="No motion and Led off" # for debugging only

    # Get the temperature and humidity values
    hum, temp= Adafruit_DHT.read_retry(sensor, pin)
    if(hum > 80 or temp > 30): # Set the alarm values
        GPIO.digitalWrite(Buzz, GPIO.HIGH)
        buzzTest = "Buzz ON"  # For debugging
    else:
        GPIO.digitalWrite(Buzz, GPIO.LOW)

    print()
    #print("_____ watch dog _____",int(value))
    print("_____ Light Level Value _____",countValue)
    print("_____ Led and Movement Detection _____",ledder)
    print("__________The current temperature and humidity______")
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, hum))
    print("_________Buzzer Status____",buzzTest)
    print()
    time.sleep(2)        

##################################################################
# Called by WebIOPi at server shutdown
##################################################################

def destroy():
    webiopi.debug("Script with macros - Destroy")
    # Reset GPIO functions
    GPIO.setFunction(LED1, GPIO.IN)
    GPIO.setFunction(LsrPin, GPIO.IN) 
    GPIO.setFunction(Buzz, GPIO.IN)
    os.system("sudo service motion stop")
##################################################################
# Macros
##################################################################

@webiopi.macro
def getData():
    global i0,i1,i2
    # Call the function that checks the input on the motion sensor pin
    # Assign it's value to a variable
    i0 = get_movement_status()
    # Call the Temperature and Humidity function and assign values to variables	
    i1, i2=get_temp()
    # Place the variables in a Python list   
    lista = i0,i1,i2
    print("lista",lista)
    return json.dumps (lista) # encode it as JSON

@webiopi.macro
def startCamera():
 #   os.system("./webcam.sh") # run bash script that takes pictures
 
    os.system("sudo service motion start") # start the WebCam server 

#-----------------------------------------------------------------
##################################################################
#-----------------------------------------------------------------

