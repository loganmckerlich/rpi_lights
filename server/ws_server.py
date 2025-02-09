import asyncio
import websockets
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)

class TrafficLight():
    def __init__(self, red_pin, yellow_pin, green_pin):
        self.red_pin = red_pin
        self.yellow_pin = yellow_pin
        self.green_pin = green_pin
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.yellow_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        self.all_off()

    def red_on(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        print("RED ON")

    def red_off(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        print("RED OFF")

    def yellow_on(self):
        GPIO.output(self.yellow_pin, GPIO.LOW)
        print("YELLOW ON")
    
    def yellow_off(self):
        GPIO.output(self.yellow_pin, GPIO.HIGH)
        print("YELLOW OFF")

    def green_on(self):
        GPIO.output(self.green_pin, GPIO.LOW)
        print("GREEN ON")

    def green_off(self):
        GPIO.output(self.green_pin, GPIO.HIGH)
        print("GREEN OFF")

    def all_off(self):
        self.red_off()
        self.yellow_off()
        self.green_off()

# Initialize traffic light object
traffic_light = TrafficLight(red_pin=17, yellow_pin=27, green_pin=22)

async def handler(websocket, path):
    message = await websocket.recv()
    print(f"Received message: {message}")

    # Handle different messages to control the GPIO
    if message == "RED_ON":
        traffic_light.red_on()
    elif message == "RED_OFF":
        traffic_light.red_off()
    elif message == "YELLOW_ON":
        traffic_light.yellow_on()
    elif message == "YELLOW_OFF":
        traffic_light.yellow_off()
    elif message == "GREEN_ON":
        traffic_light.green_on()
    elif message == "GREEN_OFF":
        traffic_light.green_off()
    elif message == "ALL_OFF":
        traffic_light.all_off()
    else:
        await websocket.send(f"Unknown command: {message}")

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
