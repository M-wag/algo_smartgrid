from houses import Houses, House
from batteries import Batteries, Battery
from typing import Type, Tuple, List
import scheduler
from path_finders import random_path_finder
import numpy as np


class Wire():

    def __init__(self, id: int, house: Type[House], battery: Type[Battery],
                 path: List[Tuple[int, int]]) -> None:
        self.id = id
        self.house = house
        self.battery = battery
        self.path = path


class Wires():

    def __init__(self) -> None:
        self.wires = {}

    def generate(self, houses: Type[Houses],
                 batteries: Type[Batteries]) -> None:
        """Generate the wires between the houses and the batteries"""

        # Get random order for iterating houses and batteries
        random_order_houses = houses.shuffle_order()
        random_order_batteries = batteries.shuffle_order()

        wire_id = 0
        for index_house in random_order_houses:
            house = houses.dict_houses[index_house]
            house_coord = house.position
            has_battery = False
            for index_battery in random_order_batteries:
                battery = batteries.dict_batteries[index_battery]
                battery_coord = battery.position
                if battery.can_connect(house.max_output):
                    self.connect(house, battery)
                    wire_path = random_path_finder(house_coord, battery_coord)
                    # Make new wire
                    wire = Wire(wire_id, house, battery, wire_path)
                    wire_id += 1
                    has_battery = True
                    break

            if has_battery is False:
                return False
        return True

    def connect(self, house, battery):
        house.connect(battery)
        battery.connect(house)

    def get_paths(self) -> List[List[Tuple[int, int]]]:
        paths = [wire.path for wire in self.wires.values()]
        return paths
