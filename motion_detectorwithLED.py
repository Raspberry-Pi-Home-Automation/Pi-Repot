import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

## Set Motion Detector Pin and Led Pin
PIR_PIN = 12
LedPin = 23
# Set Led pin and PIR pin modes
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LedPin,GPIO.OUT)

try:
   # print "PIR Module Test (CTRL+C to exit)"
   # time.sleep(1)
   # print "Ready"

    while True:
        if GPIO.input(PIR_PIN):
            print "Motion Detected"
            GPIO.output(LedPin, GPIO.HIGH)
        else:
            GPIO.output(LedPin, GPIO.LOW)
        time.sleep(0.1)

except KeyboardInterrupt:
    print " Quit"
finally:
    GPIO.cleanup()
