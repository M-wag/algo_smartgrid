from multiprocessing import allow_connection_pickling
import pandas as pd
import random
from typing import Dict, Tuple, Type, List
from batteries import Battery


class House():

    def __init__(self, position: Tuple[int, int], max_output: float, container) -> None:
        self.position = position
        self.max_output = max_output
        self.battery = None
        self.wire = None
        self.container = container

    # assign wire to house
    def assign_wire(self, wire) -> None:
        self.wire = wire

    def connect(self, battery: Type[Battery]) -> None:
        self.battery = battery
        self.container.add_connected_house(self)


class Houses():

    def __init__(self, houses_csv: str) -> None:
        self.dict_houses = {}
        self.order = None
        self.connected_houses = []
        self.load(houses_csv)

    # Load houses from csv_file into dictionary, called upon init
    def load(self, houses_csv: str) -> Dict[int, Type[House]]:
        df_houses = pd.read_csv(houses_csv)

        for id, row in df_houses.iterrows():
            position = (int(row['x']), int(row['y']))
            max_output = float(row['maxoutput'])
            self.dict_houses[id] = House(position, max_output, self)
            self.order = list(self.dict_houses.keys())

        return self.dict_houses

    def shuffle_order(self):
        random.shuffle(self.order)
        return self.order

    def get_members(self):
        return self.dict_houses.values()

    def get_member_coords(self) -> List[Tuple[int, int]]:
        member_coords = [house.position for house in self.dict_houses.values()]
        return member_coords

    def add_connected_house(self, house) -> None:
        self.connected_houses.append(house)

    def all_houses_connected(self):
        if len(self.connected_houses) == len(self.dict_houses):
            return True
        return False
