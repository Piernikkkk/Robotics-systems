import os
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import json 
from pydantic import BaseModel


load_dotenv()
app = FastAPI()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("AI_API_KEY")
    )


robot_state = {
    "x": 0,
    "y": 0,
    "battery": 100,
    "status": "waiting",
    "message": ""
}
robot_target = {
    "x": 0,
    "y": 0,
}

class Command(BaseModel):
    command: str

# Endpoint to receive commands from the frontend

@app.post("/send_command")
def receive_command(command: Command):
    global robot_state 
    global robot_target
    current_position = f"x: {robot_state['x']}, y: {robot_state['y']}"

    user_message =  ("You are a robot Valley."
                     f"Respond to the user {command} ONLY with a JSON object: {{\"x\": int, \"y\": int}}. No text around."
    )
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": user_message},
            {"role": "user", "content": f"Current position: {current_position}. Command: {command}"}
        ]
    )
    result = json.loads(response.choices[0].message.content) # get pure text from AI

    robot_target["x"] = int(result["x"])
    robot_target["y"] = int(result["y"])

    return robot_target


@app.get("/get_target")
def get_target():
    return robot_target

@app.get("/get_state")
def get_state():
    return robot_state

@app.post("/update_state")
def update_state(state: dict):
    global robot_state
    robot_state["x"] = int(state.get("x", robot_state["x"]))
    robot_state["y"] = int(state.get("y", robot_state["y"]))
    robot_state["battery"] = int(state.get("battery", 100))
    robot_state["status"] = state.get("status", "waiting")
    robot_state["message"] = state.get("message", "")
    return robot_state


#### !!!!! UPDATE ROBOT STATE WHEN HE MOVES !!!!####