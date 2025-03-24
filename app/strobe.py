import streamlit as st
import time

def strobe_controller():
    """Creates a Streamlit UI for controlling a strobe effect using traffic light toggles."""

    # Ensure session state variables exist
    if "strobe_running" not in st.session_state:
        st.session_state.strobe_running = False
    if "strobe_speed" not in st.session_state:
        st.session_state.strobe_speed = 5
    if "strobe_colors" not in st.session_state:
        st.session_state.strobe_colors = {"red": False, "yellow": False, "green": False}

    def strobe():
        """Runs the strobe effect using Streamlit's rerun mechanism."""
        while st.session_state.strobe_running:
            print("Strobing...")  # Debugging print statement

            # Turn ON all selected colors
            for color, active in st.session_state.strobe_colors.items():
                if active:
                    getattr(st.session_state.tl, f"{color}_on")()

            time.sleep(0.1 + (1 - (st.session_state.strobe_speed / 10)))  # Control speed

            # Turn OFF all selected colors
            for color, active in st.session_state.strobe_colors.items():
                if active:
                    getattr(st.session_state.tl, f"{color}_off")()

            time.sleep(0.1 + (1 - (st.session_state.strobe_speed / 10)))  # Control speed

            st.rerun()  # Refresh UI

    def stop_strobe():
        """Stops the strobe effect."""
        print("Strobe stopped")  # Debugging print statement
        st.session_state.strobe_running = False

    with st.container():
        with st.form("Strobe Controls"):
            r, y, g = st.columns(3)
            with r:
                st.session_state.strobe_colors["red"] = st.toggle("Red", st.session_state.strobe_colors["red"])
            with y:
                st.session_state.strobe_colors["yellow"] = st.toggle("Yellow", st.session_state.strobe_colors["yellow"])
            with g:
                st.session_state.strobe_colors["green"] = st.toggle("Green", st.session_state.strobe_colors["green"])
            st.session_state.strobe_speed = st.slider("Speed", 0, 10, st.session_state.strobe_speed)

            submit = st.form_submit_button("Start")

        if submit:
            st.session_state.strobe_running = True
            strobe()  # Run the strobe function in the main Streamlit loop

        if st.button("Stop"):
            stop_strobe()
