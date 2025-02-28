from light import TrafficLight
# from dance_simple import LiveAudioVisualizer
import streamlit as st
import yaml
import time
with open ('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)


st.set_page_config(
    page_title="Logans Traffic Light",     # Page title shown in browser tab
    page_icon=":vertical_traffic_light:",                 # Emoji or image icon in the browser tab
    layout="centered",                     # Choose layout: "centered" or "wide"
    initial_sidebar_state="collapsed"      # Sidebar: "auto", "expanded", or "collapsed"
)

if not st.session_state.get("approved"):
    if st.session_state.get('pw') != config['pw']:
        with st.form(key='pw'):
            st.text_input("enter password",type="password",key='pw')
            if st.form_submit_button("submit"):
                if st.session_state['pw'] != config['pw']:
                    st.error("Wrongo Bongo")
                    st.stop()
            else:
                st.stop()

st.session_state["approved"] = True


ws_address = config["wss"]

if not st.session_state.get('tl'):
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
        # st.warning(icon = ':construction_worker:' , body = 'disabled')
        st.warning(body = 'disabled')
        # ra, rb, _ = st.columns([1,1,2])
        # with ra:
        #     single = st.toggle("Single")
        # with rb:
        #     if st.button("Randomize"):
        #         st.session_state.tl.randomize(single)
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
        # def strobe_control_ui():
        #     st.header("Strobe Controls")
        #     st.session_state.tl.strobe_lights["red"] = st.checkbox("Strobe Red", st.session_state.tl.strobe_lights["red"])
        #     st.session_state.tl.strobe_lights["yellow"] = st.checkbox("Strobe Yellow", st.session_state.tl.strobe_lights["yellow"])
        #     st.session_state.tl.strobe_lights["green"] = st.checkbox("Strobe Green", st.session_state.tl.strobe_lights["green"])
        #     st.session_state.tl.strobe_sync = st.toggle("Sync Strobe", st.session_state.tl.strobe_sync)
        #     st.session_state.tl.strobe_rate = st.slider("Strobe Speed", 0.1, 2.0, st.session_state.tl.strobe_rate, 0.1)
            
        #     if st.button("Start Strobe"):
        #         st.session_state.tl.start_strobe()
        #     if st.button("Stop Strobe"):
        #         st.session_state.tl.stop_strobe()

        # strobe_control_ui()


    light_box = st.container()    
    if st.button("Reset"):
        st.session_state.tl = TrafficLight(ws_address)
        #red_pin=26, yellow_pin=20, green_pin=21
    
    with light_box:
        st.image(st.session_state.tl.virtual_light())


    # st.text(f"""
    # Red:    {st.session_state.tl.red}
    # Yellow: {st.session_state.tl.yellow}
    # Green:  {st.session_state.tl.green}
    # """)