# class house & class houses

import pandas as pd
import random
from typing import Dict, Tuple, Type
from wires import Wire
from batteries import Battery


class House():

    def __init__(self, position: Tuple[int, int], max_output: float) -> None:
        self.position = position
        self.max_output = max_output
        self.battery = None
        self.wire = None

    # assign wire to house
    def assign_wire(self, wire: Type[Wire]) -> None:
        self.wire = wire
    
    def assign_battery(self, battery: Type[Battery]) -> None:
        self.battery = battery


class Houses():

    def __init__(self):
        self.dict_houses = {}
        self.order = None

    # load houses from csv_file into dictionary
    def load(self, houses_csv) -> Dict[Type[House]]:
        df_houses = pd.read_csv(houses_csv)

        for id, row in df_houses.iterrows():
            position = (int(row['x']), int(row['y']))
            max_output = float(row['maxoutput'])
            self.dict_houses[id] = House(position, max_output)
            self.order = list(self.dict_houses.keys())

        return self.dict_houses

    def shuffle_order(self):
        random.shuffle(self.order)
