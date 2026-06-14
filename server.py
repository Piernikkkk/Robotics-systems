import os
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import json 
from pydantic import BaseModel


load_dotenv()
app = FastAPI()
"""
client = OpenAI(
    base_url="https://openrouter.ai/api/v1/rerank",
    api_key=os.getenv("AI_API_KEY")
    )
headers={
    "Authorization": f"Bearer {os.getenv("AI_API_KEY")}",
    "Content-Type": "application/json"
}
"""

robot_state = {
    "x": 0,
    "y": 0,
}
robot_target = {
    "x": 0,
    "y": 0,
}

class Command(BaseModel):
    command: str

# Endpoint to receive commands from the frontend
"""
@app.post("/send_command")
def receive_command(command: Command):
    global robot_state 
    global robot_target
    current_position = f"x: {robot_state['x']}, y: {robot_state['y']}"

    user_message =  (f"You are a robot Valley. Current position: {current_position}."
                     f"Respond to the user {command} ONLY with a JSON object: {{\"x\": int, \"y\": int}}. No text around."
    )
    
    response = client.chat.completions.create(
        model = "nvidia/llama-nemotron-rerank-vl-1b-v2:free",
        messages = [
            {"role": "system", "content": user_message},
            {"role": "user", "content": command}
        ]
    )
    ai_json_text = response.choices[0].message.content.strip().replace("```json", "").replace("```", "").strip() # get pure text from AI
    # Update the robot's target position and status based on the AI response

    # Turn JSON text into a Python robot_target 
    robot_target.update(json.loads(ai_json_text))
    return robot_target
"""

#####################################
@app.post("/send_command")
def receive_command(command: Command):
    print(command.command)

    robot_target["x"] = 5
    robot_target["y"] = 5
    return robot_target
#####################################

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
    return robot_state


#### !!!!! UPDATE ROBOT STATE WHEN HE MOVES !!!!####