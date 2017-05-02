#!/usr/bin/python
# Toshi Bass
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
 


sys.path.append("/home/pi/project/html") # Revise to your path

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
ledder="off" #just for testing

def setup():
    webiopi.debug("Script with macros - Setup")
    # Setup GPIOs
    GPIO.setFunction(LED1, GPIO.OUT)
    GPIO.setFunction(PIR_PIN, GPIO.IN)
    

##################################################################
#Setup Vars
##################################################################

i0,i1,i2,i3,i4,i5,i6,i7,i8,i9 = 0,0,0,0,0,0,0,0,0,0


##################################################################
# Define Functions
##################################################################

####### Function for Photorresistor ##############
# Counts how long it takes for the capacitor to charge  #
# In bright light capacitor charges very quick = low values #
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

#######  Function for Temperature and Humidity ######
#   Calls an Adafruit function taking in the sensor and pin #

def get_temp():
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   return humidity, temperature
 
##################################################################
# Looped by WebIOPi
##################################################################

def loop():
    #Set a variable to the count returned by the sensor function
    countValue= rc_time(LsrPin)
    # use the value of the count to set led pin to high(on) or low(off)
    #Led also turns on if motion detected
    if(countValue>100 or  GPIO.digitalRead(PIR_PIN)==GPIO.HIGH):
        GPIO.digitalWrite(LED1, GPIO.HIGH)
        ledder="Motion Detected" # for debugging only
    else:
        GPIO.digitalWrite(LED1,GPIO.LOW)
        ledder="OFF" # for debugging only

    # For debugging, get the temperature and humidity values
    hum, temp= get_temp()


    print()
    #print("_____ watch dog _____",int(value))
    print("_____ watch dog _____",countValue)
    print("_____ watch dog _____",ledder)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, hum))
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
##################################################################
# Macros
##################################################################

@webiopi.macro
def getData():
    global i0,i1,i2,i3,i4,i5,i6,i7,i8,i9
    
   # check if the led is on or off and send the value to the HTML page
    if (GPIO.digitalRead(LED1)==GPIO.HIGH or (GPIO.digitalRead(PIR_PIN)==GPIO.HIGH)):
       i0=("ON")
       i1=("Motion Detected")
    elif (GPIO.digitalRead(LED1)==GPIO.LOW or GPIO.digitalRead(PIR_PIN)==GPIO.LOW):
       i0=("OFF")   
       i1=("NO Motion Detected")
    # Call the Temperature and Humidity function and assign values to variables	

    i2, i3=get_temp()

    i9=("Toshi")
    
    lista = i0,i1,i2,i3,i4,i5,i6,i7,i8,i9
    print("lista",lista)
    return json.dumps (lista)

#-----------------------------------------------------------------
##################################################################
#-----------------------------------------------------------------
