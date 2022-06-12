from houses import House, Houses
from batteries import Batteries
from typing import Type
import scheduler
import path_finders

schedule = scheduler.random_scheduler
find_path = path_finders.random_path_finder

class Wires():
    def __init__(self) -> None:
        pass

    def generate(self, houses: Type[Houses], batteries: Type[Batteries]) -> None:
        """Generate the wires between the houses and the batteries"""
    
        #   TODO make more readable. Add function to class to just return list
        coords_houses = schedule(houses.get_coords())
        coords_batteries = schedule(batteries.get_coords())

        for house_coord in coords_houses:
            find_path(house_coord, coords_batteries)

        

class Wire():
    def __init__(self, house, battery, path) -> None:
        self.house = house
        self.battery = battery
        self.path = path

        
