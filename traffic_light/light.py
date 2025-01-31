import RPi.GPIO as GPIO
from PIL import Image, ImageDraw
from io import BytesIO
import random

# Set up GPIO
GPIO.setmode(GPIO.BCM)

class TrafficLight():
    def __init__(self, red_pin, yellow_pin, green_pin):
        # GPIO Pins for each light
        self.red_pin = red_pin
        self.yellow_pin = yellow_pin
        self.green_pin = green_pin
        
        # Set up the pins as output
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.yellow_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        
        # Turn all lights off initially
        self.all_off()
    
    def red_on(self):
        GPIO.output(self.red_pin, GPIO.LOW)  # LOW means ON
        self.red = True
        print("RED")

    def red_off(self):
        GPIO.output(self.red_pin, GPIO.HIGH)  # HIGH means OFF
        self.red = False

    def red_toggle(self):
        if self.red:
            self.red_off()
        else:
            self.red_on()

    def yellow_on(self):
        GPIO.output(self.yellow_pin, GPIO.LOW)  # LOW means ON
        self.yellow = True
        print("YELLOW")
    
    def yellow_off(self):
        GPIO.output(self.yellow_pin, GPIO.HIGH)  # HIGH means OFF
        self.yellow = False

    def yellow_toggle(self):
        if self.yellow:
            self.yellow_off()
        else:
            self.yellow_on()

    def green_on(self):
        GPIO.output(self.green_pin, GPIO.LOW)  # LOW means ON
        self.green = True
        print("GREEN")

    def green_off(self):
        GPIO.output(self.green_pin, GPIO.HIGH)  # HIGH means OFF
        self.green = False

    def green_toggle(self):
        if self.green:
            self.green_off()
        else:
            self.green_on()

    def randomize(self, single=False):
        if single:
            light_choice = random.choice(["red", "yellow", "green"])
            self.all_off()
            if light_choice == "red":
                self.red_on()
            elif light_choice == "yellow":
                self.yellow_on()
            else:
                self.green_on()
        else:
            self.red = random.choice([True, False])
            self.yellow = random.choice([True, False])
            self.green = random.choice([True, False])
            GPIO.output(self.red_pin, GPIO.LOW if self.red else GPIO.HIGH)
            GPIO.output(self.yellow_pin, GPIO.LOW if self.yellow else GPIO.HIGH)
            GPIO.output(self.green_pin, GPIO.LOW if self.green else GPIO.HIGH)

    def all_off(self):
        self.green_off()
        self.red_off()
        self.yellow_off()

    def virtual_light(self):
        width, height = 200, 400
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle([50, 50, 150, 350], fill="black")
    
        red_color = "red" if self.red else "white"
        yellow_color = "yellow" if self.yellow else "white"
        green_color = "green" if self.green else "white"

        draw.ellipse([70, 60, 130, 120], fill=red_color, outline="black")
        draw.ellipse([70, 160, 130, 220], fill=yellow_color, outline="black")
        draw.ellipse([70, 260, 130, 320], fill=green_color, outline="black")

        output = BytesIO()
        image.save(output, format="JPEG")
        output.seek(0)
        return output
