#import the GPIO library
import RPi.GPIO as GPIO
import time
# Set the GPIO numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set the pins
LsrPin = 25
LedPin = 23
# set led pin as out
GPIO.setup(LedPin,GPIO.OUT)

# function returning a count of how long
# it takes the capacitor to load based on 
# the resistance of Photoresistor
def rc_time(LsrPin):
 count=0
 GPIO.setup(LsrPin, GPIO.OUT)
 GPIO.output(LsrPin, GPIO.LOW)
 time.sleep(1) 
 GPIO.setup(LsrPin, GPIO.IN)
 while(GPIO.input(LsrPin)==GPIO.LOW):
  count +=0.01
 return count
# run the program and depending on value of count
# turn light on or off
try:
 while True:
  print rc_time(LsrPin)
  if(rc_time(LsrPin))>100:
     GPIO.output(LedPin, GPIO.HIGH)
  else:
     GPIO.output(LedPin, GPIO.LOW)  
#allow a way to interrupt the program
except KeyboardInterrupt:
 pass
# return the pins to original state
finally:
 GPIO.cleanup()
