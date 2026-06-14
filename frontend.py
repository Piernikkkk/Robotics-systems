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

placeholder = st.empty()
while True:
    try:
        response = requests.get("http://127.0.0.1:8000/get_state")
        data = response.json()
        with placeholder.container():
            st.write(f"y: {data.get('y', 0)}")
            st.write(f"x: {data.get('x', 0)}")
            st.write(f"battery: {data.get('battery', 100)}%")
            st.write(f"status: {data.get('status')}")
            st.write(f"message: {data.get('message')}")
    except Exception as e:
        st.error(f"Serever error: {e}")
    time.sleep(1)
