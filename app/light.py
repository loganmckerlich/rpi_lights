import streamlit as st
import websocket
import threading
from io import BytesIO
from PIL import Image, ImageDraw
import time

class TrafficLight():
    def __init__(self, ws_address):
        self.ws_address = ws_address
        self.ws = None
        self.connect_ws()
        time.sleep(0.5)
        self.all_off()

    def connect_ws(self):
        """ Connect to the WebSocket server on Raspberry Pi """
        self.ws = websocket.WebSocketApp(self.ws_address,
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close)
        self.ws.on_open = self.on_open
        # Run WebSocket connection in a separate thread so Streamlit doesn't freeze
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def on_message(self, ws, message):
        """ Handle incoming messages (not needed for this case, but you can use for feedback) """
        st.write(f"Received from Pi: {message}")

    def on_error(self, ws, error):
        """ Handle any errors """
        st.write(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """ Handle WebSocket closure """
        st.write("WebSocket closed.")

    def on_open(self, ws):
        """ Handle successful WebSocket connection """
        st.write("Connected to WebSocket server on Raspberry Pi.")

    def send_command(self, command):
        """ Send command to the Raspberry Pi to control GPIO """
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(command)
        else:
            print("Failed to send command, WebSocket not connected.")

    def green_toggle(self):
        if self.green:
            self.green_off()
        else:
            self.green_on()

    def yellow_toggle(self):
        if self.yellow:
            self.yellow_off()
        else:
            self.yellow_on()

    def red_toggle(self):
        if self.red:
            self.red_off()
        else:
            self.red_on()

    # GPIO control methods
    def red_on(self):
        self.red = True
        self.send_command("RED_ON")

    def red_off(self):
        self.red = False
        self.send_command("RED_OFF")

    def yellow_on(self):
        self.yellow = True
        self.send_command("YELLOW_ON")

    def yellow_off(self):
        self.yellow = False
        self.send_command("YELLOW_OFF")

    def green_on(self):
        self.green = True
        self.send_command("GREEN_ON")

    def green_off(self):
        self.green = False
        self.send_command("GREEN_OFF")

    def all_off(self):
        self.red = self.yellow = self.green = False
        self.send_command("ALL_OFF")

    # Virtual Light method
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
