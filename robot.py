import requests 
import time


class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.battery = 100
        self.status = "waiting"
        self.message = ""
    def move(self, target_x, target_y):
            # check battery level before moving
        distance_to_target = abs(target_x - self.x) + abs(target_y - self.y)
        distance_target_base = abs(target_x) + abs(target_y)
        needed_battery = distance_to_target + distance_target_base
        if self.battery <= needed_battery:
            self.status = "returning to base"
            self.message = "Battery low. Returning to base."
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
        self.send_state_update()


    def send_state_update(self):
        requests.post("http://127.0.0.1:8000/update_state", json={
            "x": self.x, "y": self.y, "battery": self.battery, "status": self.status, "message": self.message
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





