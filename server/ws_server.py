import RPi.GPIO as GPIO
import time
from websocket_server import WebsocketServer
import socket
import subprocess
import requests
import json
import yaml

with open ('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

# Set up GPIO (same as your original code)
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

# WebSocket commands to control traffic lights
def handle_client_message(client, server, message):
    """ Handle incoming WebSocket messages from client """
    print(f"Received message: {message}")

    # Define what to do based on the command received
    if message == "RED_ON":
        GPIO.output(red_pin, GPIO.LOW)  # Turn red ON

    elif message == "RED_OFF":
        GPIO.output(red_pin, GPIO.HIGH)  # Turn red OFF

    elif message == "YELLOW_ON":
        GPIO.output(yellow_pin, GPIO.LOW)  # Turn yellow ON

    elif message == "YELLOW_OFF":
        GPIO.output(yellow_pin, GPIO.HIGH)  # Turn yellow OFF

    elif message == "GREEN_ON":
        GPIO.output(green_pin, GPIO.LOW)  # Turn green ON


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

def get_ngrok_url():
    """ Get the public Ngrok URL dynamically """
    try:
        # Make a request to the Ngrok API to get the public URL
        ngrok_info = requests.get("http://localhost:4040/api/tunnels")
        ngrok_info = ngrok_info.json()

        # Extract the public URL from the Ngrok response
        public_url = ngrok_info['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print(f"Error fetching Ngrok URL: {e}")
        return None

def powered_on():
    GPIO.output(red_pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(yellow_pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(green_pin, GPIO.LOW)
    time.sleep(1)

    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(yellow_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.HIGH)



# Start the Ngrok tunnel in the background
subprocess.Popen(["ngrok", "http", "8765"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Give Ngrok a moment to start the tunnel
time.sleep(2)

# Get the public URL from Ngrok
ngrok_url = get_ngrok_url()

time.sleep(2)


if ngrok_url:
    print(f"WebSocket server running on {ngrok_url}")
    powered_on()
else:
    print("Failed to get Ngrok URL")

ip_address = "0.0.0.0" 

# Create WebSocket server on port 8765
server = WebsocketServer(host=ip_address, port=8765)

# Register the event handlers
server.set_fn_message_received(handle_client_message)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)

# Start the WebSocket server
server.run_forever()
