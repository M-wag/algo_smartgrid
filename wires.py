from houses import Houses, House
from batteries import Batteries, Battery
from typing import Type, Tuple, List
import scheduler
import path_finders
import numpy as np

grid_size = 51


schedule = scheduler.random_scheduler
find_path = path_finders.random_path_finder


class Wire():

    def __init__(self, id: int, house: Type[House], battery: Type[Battery],
                 path: List[Tuple[int, int]]) -> None:
        self.id = id
        self.house = house
        self.battery = battery
        self.path = path


class Wires():

    def __init__(self) -> None:
        self.wire_grid = np.zeros((grid_size, grid_size))
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
                    wire_path = find_path(house_coord, battery_coord)
                    # Make new wire
                    wire = Wire(wire_id, house, battery, wire_path)
                    self.add(wire)
                    wire_id += 1
                    has_battery = True
                    break

            if has_battery is False:
                return False
        return True

    def add(self, wire) -> None:
        self.wires[wire.id] = wire
        # TODO Add to wire grid

    def connect(self, house, battery):
        house.connect(battery)
        battery.connect(house)

    def get_paths(self) -> List[List[Tuple[int, int]]]:
        paths = [wire.path for wire in self.wires.values()]
        return paths
