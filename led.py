import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #use Broadcom numbers for pin
GPIO.setup(23,GPIO.OUT) #set pin 23 as output
count=0
try:
 while count<5:
  print "Led on"
  GPIO.output(23, GPIO.HIGH) #sets the pin 23 to high, or true
  time.sleep(2)
  GPIO.output(23, GPIO.LOW) #turns light off, sets pin to low or false
  time.sleep(2)
  print "Led Off"
  count += 1
except KeyboardInterrupt:
 #break program with CTRL+C, then the code in finnally will run
 pass
except:
 #Error handling code
 print "Here should be error handling code"
finally:
 GPIO.cleanup()
