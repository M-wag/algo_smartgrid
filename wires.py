from houses import Houses
from batteries import Batteries
from typing import Type, Tuple
import scheduler
import path_finders
import numpy as np

grid_size = 51


schedule = scheduler.random_scheduler
find_path = path_finders.random_path_finder

class Wires():

    def __init__(self) -> None:
        self.wire_grid = np.zeros((grid_size, grid_size))
        self.wires = {}

    def generate(self, houses: Type[Houses], batteries: Type[Batteries]) -> None:
        """Generate the wires between the houses and the batteries"""
        
        # Get coordinates for all houses and batteries
        houses_with_coords = {house : house.position for house in houses.get_members()}  
        batteries_with_coords = {battery : battery.position for battery in batteries.get_members()}

        # TODO shuffle dictionary
        # # Put both dictionaries through the scheduler
        # coords_houses = schedule(coords_houses)
        # coords_batteries = schedule(coords_batteries)

        wire_id = 0
        iterations = 0
        while True:
            #Pairing Algorithm 
            # Iterate through houses
            for ho, ho_c in houses_with_coords.items():
                for bat, bat_c in batteries_with_coords.items():
                    if bat.can_connect(ho.max_output):
                        # Save the connectable entities
                        house = ho
                        house_coord = ho_c
                        battery = bat
                        battery_coord = bat_c
                        # Add to wire id  
                        wire_id += 1
                        break
            # Remove connected house from houses dictionary
            houses_with_coords.pop(house)

            self.connect(house, battery)
            wire_path = find_path(house_coord, battery_coord)
            # Make new wire
            wire = Wire(wire_id, house, battery, wire_path)
            self.add(wire)

            # Break if all houses are connected or iterations > 250
            # TODO make funtion in Houses which returns whether all houses are connected
            if len(houses_with_coords) == 0 or iterations > 250:
                break

    def add(self, wire) -> None:
        self.wires[wire.id] = wire
        #TODO Add to wire grid

    def connect(self, house, battery):
        house.connect(battery)
        battery.connect(house)
    
    def get_paths(self) -> list[list[Tuple[int, int]]]:
        paths = [wire.path for wire in self.wires.values()]
        return paths

class Wire():
    def __init__(self, id, house, battery, path) -> None:
        self.id = id
        self.house = house
        self.battery = battery
        self.path = path

        
