import streamlit as st
import requests

st.title("Robot Valley")

user_command = st.text_input("Ask Valley to move to a location (e.g., 'move to (3, 4))")
if st.button("Enter"):
    # Send a request to the backend to move the robot
    requests.post("http://127.0.0.1:8000/send_command", json={"command": user_command})
 

st.write("---")


response = requests.get("http://127.0.0.1:8000/get_target")
data = response.json()
x_position = data.get("x", 0)
y_position = data.get("y", 0)
battery = 100
status = "Idle"


st.write(f"Current Position: (x:{x_position}, y:{y_position})")
st.write(f"Battery Level: {battery}%")
st.write(f"Status: {status}")



