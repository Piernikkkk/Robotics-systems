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
            self.send_state_update()
            return
        
            # Move towards the target
        self.status = "moving to the target"
        while self.x != target_x:
            if self.x < target_x:
                self.x += 1
            else:
                self.x -= 1
            self.battery -= 1
            print(f"x: {self.x}")
            self.send_state_update()
            time.sleep(1)

        while self.y != target_y:
            if self.y < target_y:
                self.y += 1
            else:
                self.y -= 1
            self.battery -= 1
            print(f"y: {self.y}")
            self.send_state_update()
            time.sleep(1)

            self.status = "at the target"
            print(f"Right here! Position: ({self.x}, {self.y}),\nBattery: {self.battery}%, Status: {self.status}")


    def send_state_update(self):
        requests.post("http://127.0.0.1:8000/update_state", json={
            "x": self.x, "y": self.y
            })



valley = Robot()
while True:
    response = requests.get("http://127.0.0.1:8000/get_target")
    target = response.json()

    target_x = int(target["x"])
    target_y = int(target["y"])
    
    if valley.x != target_x or valley.y != target_y:
        valley.move(target_x, target_y)

    time.sleep(1)





