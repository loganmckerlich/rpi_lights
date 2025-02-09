import RPi.GPIO as GPIO
import time
from websocket_server import WebsocketServer
import socket

ip_address = socket.gethostbyname(socket.gethostname())

# Set up GPIO (same as your original code)
GPIO.setmode(GPIO.BCM)
red_pin = 17
yellow_pin = 27
green_pin = 22

# Set up GPIO pins
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# Initialize all pins to OFF
GPIO.output(red_pin, GPIO.HIGH)
GPIO.output(yellow_pin, GPIO.HIGH)
GPIO.output(green_pin, GPIO.HIGH)

# WebSocket commands to control traffic lights
def handle_client_message(client, server, message):
    """ Handle incoming WebSocket messages from client """
    print(f"Received message: {message}")

    # Define what to do based on the command received
    if message == "RED_ON":
        GPIO.output(red_pin, GPIO.LOW)  # Turn red ON
        GPIO.output(yellow_pin, GPIO.HIGH)  # Turn yellow OFF
        GPIO.output(green_pin, GPIO.HIGH)  # Turn green OFF
    elif message == "RED_OFF":
        GPIO.output(red_pin, GPIO.HIGH)  # Turn red OFF
    elif message == "YELLOW_ON":
        GPIO.output(yellow_pin, GPIO.LOW)  # Turn yellow ON
        GPIO.output(red_pin, GPIO.HIGH)  # Turn red OFF
        GPIO.output(green_pin, GPIO.HIGH)  # Turn green OFF
    elif message == "YELLOW_OFF":
        GPIO.output(yellow_pin, GPIO.HIGH)  # Turn yellow OFF
    elif message == "GREEN_ON":
        GPIO.output(green_pin, GPIO.LOW)  # Turn green ON
        GPIO.output(red_pin, GPIO.HIGH)  # Turn red OFF
        GPIO.output(yellow_pin, GPIO.HIGH)  # Turn yellow OFF
    elif message == "GREEN_OFF":
        GPIO.output(green_pin, GPIO.HIGH)  # Turn green OFF
    elif message == "ALL_OFF":
        GPIO.output(red_pin, GPIO.HIGH)  # Turn all OFF
        GPIO.output(yellow_pin, GPIO.HIGH)
        GPIO.output(green_pin, GPIO.HIGH)
    else:
        print(f"Unknown command: {message}")

def new_client(client, server):
    """ Handle new client connection """
    print(f"New client connected: {client['address']}")

def client_left(client, server):
    """ Handle client disconnect """
    print(f"Client disconnected: {client['address']}")


# Create WebSocket server on port 8765
server = WebsocketServer(host=ip_address, port=8765)

# Register the event handlers
server.set_fn_message_received(handle_client_message)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)

# Start the WebSocket server


print(f"WebSocket server running on ws://{ip_address}:8765")
server.run_forever()
