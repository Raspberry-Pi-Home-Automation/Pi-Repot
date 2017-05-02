import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

PIR_PIN = 12
LedPin = 23

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LedPin,GPIO.OUT)


def MOTION(PIR_PIN):
    print "Motion Detected"
    GPIO.output(LedPin, GPIO.HIGH)

print "PIR Module Test (CTRL+C to exit)"
time.sleep(2)
print "Ready"
GPIO.output(LedPin, GPIO.LOW)

try:
   # use a GPIO interrupt function with call back to separate function
   # more efficient as program waits for GPIO event and not continually
   # listens to the pin
   # it works as edge detection, detecting changes in state low to high, high to low
   GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
   
   # check for 1 instead of True
   # using 1 saves resources as it skips the variable check on True
   while 1:
        GPIO.output(LedPin, GPIO.LOW)
        time.sleep(100)
#   GPIO.output(LedPin, GPIO.LOW)



except KeyboardInterrupt:
    print " Quit"
    GPIO.cleanup()
