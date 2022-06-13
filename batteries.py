import pandas as pd
import random
from typing import Tuple, Type, List, Dict


class Battery:

    def __init__(self, position: Tuple[int, int], capacity: float) -> None:
        self.position = position
        self.capacity = capacity
        self.total_input = 0
        self.houses = []

    def can_connect(self, house_output: float) -> bool:
        if self.total_input + house_output > self.capacity:
            return False
        return True

    def connect(self, house) -> None:
        self.houses.append(house)
        self.total_input += house.max_output


class Batteries:

    def __init__(self, batteries_csv: str) -> None:
        self.dict_batteries = {}
        self.order = None
        self.load(batteries_csv)

    def load(self, batteries_csv: str) -> Dict[int, Type[Battery]]:
        df_batteries = pd.read_csv(batteries_csv)

        for id, row in df_batteries.iterrows():
            x, y = row['positie'].split(',')
            capacity = int(row['capaciteit'])
            self.dict_batteries[id] = Battery((int(x), int(y)), capacity)
            self.order = list(self.dict_batteries.keys())

        return self.dict_batteries

    def shuffle_order(self) -> None:
        random.shuffle(self.order)
        return self.order

    def get_members(self):
        return self.dict_batteries.values()

    def get_member_coords(self) -> List[Tuple[int, int]]:
        member_coords = [battery.position for battery in
                         self.dict_batteries.values()]
        return member_coords
