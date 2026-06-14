import streamlit as st
import requests
import time

st.title("Robot Valley")

user_command = st.text_input("Ask Valley to move to a location (e.g., 'move to (3, 4))")
if st.button("Enter"):
    # Send a request to the backend to move the robot
    if user_command:
        requests.post("http://127.0.0.1:8000/send_command", json={"command": user_command})
        st.success(f"Command sent: {user_command}")
        time.sleep(1)
 

st.write("---")

st.fragment(run_every=1)
def show_position():
    response = requests.get("http://127.0.0.1:8000/get_state")
    data = response.json()
    x_position = data.get("x", 0)
    y_position = data.get("y", 0)


    st.write(f"Current Position: (x:{x_position}, y:{y_position})")
show_position()


