import requests 
import time

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.battery = 100
        self.status = "waiting"

    def move(self, target_x, target_y):
            # check battery level before moving
        if self.battery <= (self.x + self.y + 1):
            self.status = "returning to base"
            print("Battery low. Returning to base.")
            # Code to return to base 
            self.x = 0
            self.y = 0
            self.battery = 1
            self.status = "at the base"
            print(f"Back at base. Position: ({self.x}, {self.y}),\nBattery: {self.battery}%, Status: {self.status}")
        else:
            # Move towards the target
            self.status = "moving to the target"
            while self.x != target_x:
                if self.x < target_x:
                    self.x += 1
                else:
                    self.x -= 1
                self.battery -= 1
                print(f"x: {self.x}")

            while self.y != target_y:
                if self.y < target_y:
                    self.y += 1
                else:
                    self.y -= 1
                self.battery -= 1
                print(f"y: {self.y}")
            self.status = "at the target"
            print(f"Right here! Position: ({self.x}, {self.y}),\nBattery: {self.battery}%, Status: {self.status}")



# Infinity request loop for a new target 
valley = Robot()
while True:
    response = requests.get("http://127.0.0.1:8000/get_target")
    target = response.json()
    valley.move(target["x"], target["y"])

    requests.post("http://127.0.0.1:8000/update_state", json={
        "x": valley.x, "y": valley.y
        })
    time.sleep(2)  

