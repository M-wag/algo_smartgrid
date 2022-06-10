import pandas as pd
import random 
class Houses:
    def __init__(self, file):
        self.house_list = self.load(file)

    def load(self, file):
        df_houses = pd.read_csv(file)
        houses = []
        for index, row in df_houses.iterrows():
            x = int(row['x'])
            y = int(row['y'])
            house = House(index, (x, y), row['maxoutput'])
            houses.append(house)

        return houses

    def shuffle(self):
        self.battery_list = random.shuffle(self.battery_list)

class House():
    def __init__(self, id , position, max_output):
        self.id = id
        self.position = position
        self.max_output = max_output
        self.battery = None

    def connect(self, battery):
        self.battery = battery

