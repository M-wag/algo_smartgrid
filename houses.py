import pandas as pd
import random
from typing import Dict, Tuple, Type


class House():

    def __init__(self, position: Tuple[int, int], max_output: float) -> None:
        self.position = position
        self.max_output = max_output
        self.battery = None
        self.wire = None

    # assign wire to house (self.battery can be assigned here as well)
    def assign_wire(self, wire) -> None:
        self.wire = wire


class Houses():

    def __init__(self):
        self.dict_houses = {}
        self.order = None

    # load houses from csv_file into dictionary
    def load(self, houses_csv) -> Dict[int, Type[House]]:
        df_houses = pd.read_csv(houses_csv)

        for id, row in df_houses.iterrows():
            position = (int(row['x']), int(row['y']))
            max_output = float(row['maxoutput'])
            self.dict_houses[id] = House(position, max_output)
            self.order = list(self.dict_houses.keys())

        return self.dict_houses

    def shuffle_order(self):
        random.shuffle(self.order)

    def get_houses(self) -> None:
        return self.dict_houses
    
    def get_coords(self):
        houses = list(self.dict_houses.values())
        coord_houses = [house.position for house in houses]
        return coord_houses