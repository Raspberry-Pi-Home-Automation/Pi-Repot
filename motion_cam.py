import RPi.GPIO as GPIO
import time
from picamera import PiCamera
GPIO.setmode(GPIO.BCM)
camera = PiCamera()

PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(1)
    print "Ready"

    while True:
        if GPIO.input(PIR_PIN):
            print "Motion Detected"
            camera.start_preview()
        time.sleep(1)

except KeyboardInterrupt:
    print " Quit"
    camera.stop_preview()
    GPIO.cleanup()
