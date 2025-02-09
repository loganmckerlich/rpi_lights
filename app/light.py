import streamlit as st
import websocket
import threading

class TrafficLight():
    def __init__(self, ws_address):
        self.ws_address = ws_address
        self.ws = None
        self.connect_ws()
    
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
        if self.ws and self.ws.sock.connected:
            self.ws.send(command)
        else:
            st.write("Not connected to WebSocket server.")

    def red_on(self):
        self.send_command("RED_ON")
    
    def red_off(self):
        self.send_command("RED_OFF")
    
    def yellow_on(self):
        self.send_command("YELLOW_ON")
    
    def yellow_off(self):
        self.send_command("YELLOW_OFF")
    
    def green_on(self):
        self.send_command("GREEN_ON")
    
    def green_off(self):
        self.send_command("GREEN_OFF")
    
    def all_off(self):
        self.send_command("ALL_OFF")