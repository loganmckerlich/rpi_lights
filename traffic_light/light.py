from PIL import Image, ImageDraw
from io import BytesIO
import random

class TrafficLight():
    def __init__(self):
        self.all_off()
    
    def red_on(self):
        # eventually this will control the light
        self.red = True
        print("RED")

    def red_off(self):
        self.red = False

    def red_toggle(self):
        if self.red:
            self.red_off()
        else:
            self.red_on()

    def yellow_on(self):
        # eventually this will control the light
        self.yellow = True
        print("YELLOW")
    
    def yellow_off(self):
        self.yellow = False

    def yellow_toggle(self):
        if self.yellow:
            self.yellow_off()
        else:
            self.yellow_on()

    def green_on(self):
        # eventually this will control the light
        self.green = True
        print("GREEN")

    def green_off(self):
        self.green = False

    def green_toggle(self):
        if self.green:
            self.green_off()
        else:
            self.green_on()

    def randomize(self,single=False):
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

    def all_off(self):
        self.green_off()
        self.red_off()
        self.yellow_off()

    def virtual_light(self):
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
