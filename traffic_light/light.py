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
        # Control physical light via GPIO
        GPIO.output(self.red_pin, GPIO.HIGH)
        self.red = True
        print("RED")

    def red_off(self):
        # Control physical light via GPIO
        GPIO.output(self.red_pin, GPIO.LOW)
        self.red = False

    def red_toggle(self):
        if self.red:
            self.red_off()
        else:
            self.red_on()

    def yellow_on(self):
        # Control physical light via GPIO
        GPIO.output(self.yellow_pin, GPIO.HIGH)
        self.yellow = True
        print("YELLOW")
    
    def yellow_off(self):
        # Control physical light via GPIO
        GPIO.output(self.yellow_pin, GPIO.LOW)
        self.yellow = False

    def yellow_toggle(self):
        if self.yellow:
            self.yellow_off()
        else:
            self.yellow_on()

    def green_on(self):
        # Control physical light via GPIO
        GPIO.output(self.green_pin, GPIO.HIGH)
        self.green = True
        print("GREEN")

    def green_off(self):
        # Control physical light via GPIO
        GPIO.output(self.green_pin, GPIO.LOW)
        self.green = False

    def green_toggle(self):
        if self.green:
            self.green_off()
        else:
            self.green_on()

    def randomize(self, single=False):
        if single:
            # Ensure only one light is on at a time
            light_choice = random.choice(["red", "yellow", "green"])

            # Turn the chosen light on
            if light_choice == "red":
                self.yellow_off()
                self.green_off()
                self.red_on()
            elif light_choice == "yellow":
                self.green_off()
                self.red_off()
                self.yellow_on()
            else:
                self.yellow_off()
                self.red_off()
                self.green_on()
        else:
            # Multiple lights can be on
            self.red = random.choice([True, False])
            self.yellow = random.choice([True, False])
            self.green = random.choice([True, False])

            # Reflect changes on the physical lights
            GPIO.output(self.red_pin, GPIO.HIGH if self.red else GPIO.LOW)
            GPIO.output(self.yellow_pin, GPIO.HIGH if self.yellow else GPIO.LOW)
            GPIO.output(self.green_pin, GPIO.HIGH if self.green else GPIO.LOW)

    def all_off(self):
        # Turn off all lights (virtual + physical)
        self.green_off()
        self.red_off()
        self.yellow_off()

    def virtual_light(self):
        # Generate virtual light image
        width, height = 200, 400
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Draw the stoplight body
        draw.rectangle([50, 50, 150, 350], fill="black")
    
        # Determine light colors based on arguments
        red_color = "red" if self.red else "white"
        yellow_color = "yellow" if self.yellow else "white"
        green_color = "green" if self.green else "white"

        # Draw the red light
        draw.ellipse([70, 60, 130, 120], fill=red_color, outline="black")

        # Draw the yellow light
        draw.ellipse([70, 160, 130, 220], fill=yellow_color, outline="black")

        # Draw the green light
        draw.ellipse([70, 260, 130, 320], fill=green_color, outline="black")

        output = BytesIO()
        image.save(output, format="JPEG")
        output.seek(0)
        return output
