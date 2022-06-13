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

        # Get coordinates for all houses and batteries
        houses_with_coords = {house: house.position for house in houses.get_members()}                 # noqa: E501
        batteries_with_coords = {battery: battery.position for battery in batteries.get_members()}     # noqa: E501

        # TODO shuffle dictionary
        # # Put both dictionaries through the scheduler
        # coords_houses = schedule(coords_houses)
        # coords_batteries = schedule(coords_batteries)

        wire_id = 0
        iterations = 0

        # !!! the while-loop seems unnecessary for our random-version !!!

        while True:
            # Pairing Algorithm
            # Iterate through houses
            for house, house_coord in houses_with_coords.items():
                for battery, battery_coord in batteries_with_coords.items():
                    if battery.can_connect(house.max_output):
                        break
                break
            # Remove connected house from houses dictionary
            houses_with_coords.pop(house)

            self.connect(house, battery)
            wire_path = find_path(house_coord, battery_coord)
            # Make new wire
            wire = Wire(wire_id, house, battery, wire_path)
            self.add(wire)
            wire_id += 1

            # Break if all houses are connected or iterations > 250
            if houses.all_houses_connected() or iterations > 250:
                break

    def add(self, wire) -> None:
        self.wires[wire.id] = wire
        # TODO Add to wire grid

    def connect(self, house, battery):
        house.connect(battery)
        battery.connect(house)

    def get_paths(self) -> List[List[Tuple[int, int]]]:
        paths = [wire.path for wire in self.wires.values()]
        return paths
