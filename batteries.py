import pandas as pd
import random 
class Batteries:
    def __init__(self, file):
        self.battery_list = self.load(file)
        self.shuffle()

    def load(self, file):
        batteries = []
        df_batteries =  pd.read_csv(file)
        for index, row in df_batteries.iterrows():
            x, y = row['positie'].split(',')
            battery = Battery(index, (int(x), int(y)), row['capaciteit'])
            batteries.append(battery)
        
        return batteries

    def shuffle(self):
        self.battery_list = random.shuffle(self.battery_list)

class Battery:
    def __init__(self, id, position, capacity):
        self.id = id
        self.position = position
        self.capacity = capacity
        self.total_input = 0
        self.houses = []
    
    def can_connect(self, house_output):
        if self.total_input + house_output > self.capacity:
            return False
        else:
            return True

    def connect(self, house):
        self.houses.append(house)
        self.total_input += house.max_output