# class house & class houses

import pandas as pd
from typing import Dict, Tuple, Type


class House():

    def __init__(self, position: Tuple[int, int], max_output: int) -> None:
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

    # load houses from csv_file into dictionary
    def load(self, houses_csv) -> Dict[Type[House]]:
        df_houses = pd.read_csv(houses_csv)

        for house_id, row in df_houses.iterrows():
            position = (int(row['x']), int(row['y']))
            max_output = int(row['maxoutput'])
            self.dict_houses[house_id] = House(position, max_output)

        return self.dict_houses
