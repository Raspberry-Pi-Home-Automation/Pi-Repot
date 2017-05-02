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

LED1 = 23
LsrPin = 25
ledder="off"


def setup():
    webiopi.debug("Script with macros - Setup")
    # Setup GPIOs
    GPIO.setFunction(LED1, GPIO.OUT)
    

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

    
##################################################################
# Looped by WebIOPi
##################################################################

def loop():
    #Set a variable to the count returned by the sensor function
    countValue= rc_time(LsrPin)
    # use the value of the count to set led pin to high(on) or low(off)
    if(countValue>100):
        GPIO.digitalWrite(LED1, GPIO.HIGH)
        ledder="ON" # for debugging only
    else:
        GPIO.digitalWrite(LED1,GPIO.LOW)
        ledder="OFF" # for debugging only
    
    print()
    #print("_____ watch dog _____",int(value))
    print("_____ watch dog _____",countValue)
    print("_____ watch dog _____",ledder)
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
    if (GPIO.digitalRead(LED1)==GPIO.HIGH):
       i0=("ON")
    elif (GPIO.digitalRead(LED1)==GPIO.LOW):
       i0=("OFF")   
    
    i1=12345


    i9=("Toshi")
    
    lista = i0,i1,i2,i3,i4,i5,i6,i7,i8,i9
    print("lista",lista)
    return json.dumps (lista)

#-----------------------------------------------------------------
##################################################################
#-----------------------------------------------------------------
