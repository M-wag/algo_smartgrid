# class Battery & class Batteries

import pandas as pd
import random
from typing import Tuple, Type
from houses import House


class Battery:

    def __init__(self, position: Tuple[int, int], capacity: float) -> None:
        self.position = position
        self.capacity = capacity
        self.total_input = 0
        self.houses = set()

    def can_connect(self, house_output: float) -> bool:
        if self.total_input + house_output > self.capacity:
            return False
        return True

    def connect(self, house: Type[House]) -> None:
        self.houses.add(house)
        self.total_input += house.max_output


class Batteries:

    def __init__(self) -> None:
        self.dict_batteries = {}
        self.order = None

    def load(self, file) -> None:
        df_batteries = pd.read_csv(file)

        for id, row in df_batteries.iterrows():
            x, y = row['positie'].split(',')
            capacity = int(row['capaciteit'])
            self.dict_batteries[id] = Battery((int(x), int(y)), capacity)
            self.order = list(self.dict_batteries.keys())

        return self.dict_batteries

    def shuffle_order(self) -> None:
        random.shuffle(self.order)
