import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
red_pin=26
yellow_pin=20
green_pin=21

# Set up GPIO pins
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# Initialize all pins to OFF
GPIO.output(red_pin, GPIO.HIGH)
GPIO.output(yellow_pin, GPIO.HIGH)
GPIO.output(green_pin, GPIO.HIGH)


# Turn all ON
# Initialize all pins to OFF
GPIO.output(red_pin, GPIO.LOW)
GPIO.output(yellow_pin, GPIO.LOW)
GPIO.output(green_pin, GPIO.LOW)

time.sleep(5)
# TUrn all back off
GPIO.output(red_pin, GPIO.HIGH)
GPIO.output(yellow_pin, GPIO.HIGH)
GPIO.output(green_pin, GPIO.HIGH)