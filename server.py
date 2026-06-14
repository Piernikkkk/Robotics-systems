import os
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import json 

load_dotenv()
app = FastAPI()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("AI_API_KEY")
    )

robot_state = {
    "x": 0,
    "y": 0,
}
robot_target = {
    "x": 0,
    "y": 0,
}

# Endpoint to receive commands from the frontend
@app.post("/send_command")
def receive_command(command: str):
    global robot_state 
    global robot_target
    current_position = f"x: {robot_state['x']}, y: {robot_state['y']}"

    user_message =  (f"You are a robot Valley. Current position: {current_position}."
                     f"Respond to the user {command} ONLY with a JSON object: {{\"x\": int, \"y\": int}}. No text around."
    )
    
    response = client.chat.completions.create(
        model = "meta-llama/llama-3-8b-instruct:free",
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

@app.get("/get_target")
def get_target():
    global robot_target
    return robot_target

@app.post("/update_state")
def update_state(state: dict):
    global robot_state
    robot_state.update(state)
    return robot_state


#### !!!!! UPDATE ROBOT STATE WHEN HE MOVES !!!!####