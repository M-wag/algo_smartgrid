from houses import Houses, House
from batteries import Batteries, Battery
from typing import Type, Tuple, List, Dict
from path_finders import random_path_finder
from copy import deepcopy


class Wire():
    """
    A class to represent a wire.

    ...

    Attributes
    ----------
    id : int
        the wires id
    house : Type[House]
        the House object connected to the wire
    battery : Type[Battery]
        the Battery object connected to the wire
    path : List[Tuple[int, int]]
        a list of coordinates along which the wire is laid
    """

    def __init__(self, id: int, house: Type[House], battery: Type[Battery],
                 path: List[Tuple[int, int]]) -> None:
        self.id = id
        self.house = house
        self.battery = battery
        self.path = path

class Shared_wire:
    def __init__(self, house, battery, path):
        self.house_list = []
        self.house_list.append(house)
        self.battery = battery
        self.path = set(path)

class Wires():
    """
    A class to represent a collection of wires.

    ...

    Attributes
    ----------
    wires : Dict[int, Type[Wire]]
        a dictionary with all Wire objects contained

    Methods
    -------
    generate(self, houses: Type[Houses],
             batteries: Type[Batteries]) -> bool:
        generates wires between the houses and the batteries,
        order is randomly generated and function returns whether
        all houses can be connected or not.
    total_wires_segments(self) -> int:
        returns the total amount of wire segments
    connect(self, house: Type[House], battery: Type[Battery]) -> None:
        calls the "connect" method for the house and battery
    get_paths(self) -> List[List[Tuple[int, int]]]:
        returns a list of the paths of all wires contained
    """

    def __init__(self) -> None:
        self.wires = {}
        self.shared_wires = {}
        self.wire_segments = set()

    def generate(self, houses: Type[Houses],
                 batteries: Type[Batteries]) -> bool:

        # Get random order for iterating houses and batteries
        random_order_houses = houses.shuffle_order()
        random_order_batteries = batteries.shuffle_order()

        wire_id = 0
        
        # Iterate through each house them battery
        for house_index in random_order_houses:
            house = houses.dict_houses[house_index]
            has_battery = False
            for battery_index in random_order_batteries:
                battery = batteries.dict_batteries[battery_index]
                if battery.can_connect(house.max_output):
                    wire = self.generate_wire(wire_id, house, battery)
                    self.wires[wire_id] = wire
                    wire_id += 1
                    has_battery = True
                    break
            if has_battery is False:
                return False
        return True
    
    def generate_wire(self, wire_id, house, battery) -> Type[Wire]:
        self.connect(house, battery)
        wire_path = random_path_finder(house.position,
                                        battery.position,
                                        self.wire_segments)
        # Make new wire
        wire = Wire(wire_id, house, battery, wire_path)
        return wire

    def total_wires_segments(self) -> int:
        return len(self.wire_segments)

    def connect(self, house: Type[House], battery: Type[Battery]) -> None:
        house.connect(battery)
        battery.connect(house)

    def get_paths(self) -> List[List[Tuple[int, int]]]:
        paths = [wire.path for wire in self.wires.values()]
        return paths
    
    def swap(self, first_house, second_house) -> Dict[int, Type[Wire]]:
        first_battery = first_house.battery
        second_battery = second_house.battery

        #   Connect the first house to the second battery and the second house to the first battery
        if first_battery.can_connect(second_house) == False:
            return False
        if second_battery.can_connect(first_house) == False:
            return False

        h1_b2_wire = self.generate_wire(first_house.id, first_house, second_battery)
        h2_b1_wire = self.generate_wire(second_house.id, second_house, first_battery)

        #   Copy wires and replace the wires of passed houses
        swapped_grid = deepcopy(self.wires)
        swapped_grid[h1_b2_wire.id] = h1_b2_wire
        swapped_grid[h2_b1_wire ] = h2_b1_wire 

        return swapped_grid


    def share_wires(self):
        id = 0
        for index, wire in self.wires.items():
            count = 0
            if index == 0:
                shared = Shared_wire(wire.house, wire.battery, wire.path)
                self.shared_wires[id] = shared
                id += 1
                count += 1
            else:
                path = set(wire.path)
                for index_share, shared_wire in self.shared_wires.items():
                    if wire.battery == shared_wire.battery and len(shared_wire.path & path) >= 2:
                        shared_wire.path = shared_wire.path.union(path)
                        shared_wire.house_list.append(wire.house)
                        count = 1
            if count == 0:
                shared = Shared_wire(wire.house, wire.battery, wire.path)
                self.shared_wires[id] = shared
                id += 1

