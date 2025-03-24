from light import TrafficLight
# from dance_simple import LiveAudioVisualizer
import streamlit as st
import yaml
import time
import boto3
import os
import random as rand
from strobe import strobe_controller

st.set_page_config(
    page_title="Logans Traffic Light",     # Page title shown in browser tab
    page_icon=":vertical_traffic_light:",                 # Emoji or image icon in the browser tab
    layout="centered",                     # Choose layout: "centered" or "wide"
    initial_sidebar_state="collapsed"      # Sidebar: "auto", "expanded", or "collapsed"
)

def establish_ssm():
    if not st.session_state.get('ssm'):
        try:
            st.session_state.ssm = boto3.client("ssm") 
            print('Connected to ssm')
        except:
            print("failed connect to ssm")

def establish_wss():
    try:
        response = st.session_state.ssm.get_parameter(Name="/traffic-light/ngrok_url")
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            wss = response["Parameter"]["Value"].replace('https','wss')
            print("WSS address from SSM", wss)
            print("got wss from aws")
            st.session_state.wss = wss
            st.rerun()
        else:
            print(f'SSM call failed - {response["ResponseMetadata"]["HTTPStatusCode"]}')
    except st.session_state.ssm.exceptions.ParameterNotFound:
        print("wss address not found in SSM.")

# secrets to env
for k,v in st.secrets.items():
    os.environ[k] = v

# sign in camoflauged as a random questino
st.sidebar.text_input(
    label = 'What is your fav color?',
    type = 'password',
    key = 'user_input'
)

if st.session_state.user_input == os.environ["pw"]:
    connect = True
else:
    connect = False
    if len(st.session_state.get('user_input')) > 0:
        st.sidebar.caption(f"your favorite color is {st.session_state.user_input}")

if connect and not st.session_state.get("wss"):
    establish_ssm()
    establish_wss()

if st.session_state.get('wss'):
    st.caption('You know the forbidden color. Connected to Websocket Server through NGROK')
else:
    st.caption('Have fun playing with this stop light rendering')

ws_address = st.session_state.get("wss")

if not st.session_state.get('tl') or (st.session_state.tl.ws_address == None and ws_address is not None):
    st.session_state.tl = TrafficLight(ws_address)

# if not st.session_state.get('aud'):
#     st.session_state.aud = LiveAudioVisualizer()

if __name__ == "__main__":
    toggle, random, dance, strobe= st.tabs(['toggle','random','dance','strobe'])
    with toggle:
        tr,ty,tg,_ = st.columns([1,1,1,5])
        with tr:
            if st.button('red'):
                st.session_state.tl.red_toggle()
        with ty:
            if st.button('yellow'):
                st.session_state.tl.yellow_toggle()
        with tg:
            if st.button('green'):
                st.session_state.tl.green_toggle()

    with random:
        options = [
            st.session_state.tl.red_on,
            st.session_state.tl.yellow_on,
            st.session_state.tl.green_on
        ]


        ra, rb, _ = st.columns([1,1,2])
        with ra:
            single = st.toggle("Single")
        with rb:
            if st.button("Randomize"):
                st.session_state.tl.all_off()
                time.sleep(0.1)
                if single:
                    st.caption('new')
                    r = rand.randint(0,2)
                    options[r]()
                    
                else:
                    if rand.choice([True, False]):
                        st.session_state.tl.red_on()
                    if rand.choice([True, False]):
                        st.session_state.tl.yellow_on()
                    if rand.choice([True, False]):
                        st.session_state.tl.green_on()
    with dance:
        st.warning(body = 'disabled')
        # if st.button("Start/Stop"):
        #     st.session_state.aud.toggle()
        # st.text(st.session_state.aud.BPM_EST)
        # placeholder = st.empty()
        # with st.form(key = 'Audio Values'):
        #     NORMALIZE  = st.toggle('Normalize')
        #     REDUCTION_VAL = st.number_input("Smoothing On Plot",min_value = 0, max_value = 10, step = 1, value = 0)
        #     TRIM = st.number_input("Values to Display" ,min_value = 50, max_value = 1000, step = 50, value = 500)
        #     BEAT_THRESHOLD = st.number_input("Beat Detection Sensitivity" ,min_value = 0.0, max_value = 15.0, step = 0.1, value = 5.0)

        #     if st.form_submit_button('Apply'):
        #         st.session_state.aud.NORMALIZE = NORMALIZE
        #         st.session_state.aud.REDUCTION_VAL = REDUCTION_VAL
        #         st.session_state.aud.TRIM = TRIM
        #         st.session_state.aud.BEAT_THRESHOLD = BEAT_THRESHOLD

        # st.session_state.aud.main(placeholder)

    with strobe:
        st.warning(body = 'disabled')
        # strobe_controller() 
            
        

    light_box = st.container()    
    if st.button("Reset"):
        with st.spinner('Reseting light'):
            time.sleep(0.5)
            st.session_state.tl = TrafficLight(ws_address)
    
    with light_box:
        st.image(st.session_state.tl.virtual_light())


    # st.text(f"""
    # Red:    {st.session_state.tl.red}
    # Yellow: {st.session_state.tl.yellow}
    # Green:  {st.session_state.tl.green}
    # """)