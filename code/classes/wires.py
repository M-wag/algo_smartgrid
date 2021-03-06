from typing import Type, Tuple, List, Dict
from code.algorithms.path_finders import hor_vert_pathfinder, straight_pathfinder
from .wire import Wire, Shared_wire

Coordinate = Tuple[int, int]


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

    def __init__(self, type_wires: str) -> None:
        self.wires = {}
        self.shared_wires = {}
        self.path_type = type_wires

    def generate(self, houses, batteries) -> bool:
        '''Generate a grid'''
        # Get random order for iterating houses and batteries
        random_order_houses = houses.shuffle_order()
        random_order_batteries = batteries.shuffle_order()

        self.wires = {}
        self.shared_wires = {}

        # Iterate through each house them battery
        for house_index in random_order_houses:
            house = houses.dict_houses[house_index]
            has_battery = False
            for battery_index in random_order_batteries:
                battery = batteries.dict_batteries[battery_index]
                if battery.can_connect(house.max_output):
                    self.connect(house, battery)
                    has_battery = True
                    break
            if has_battery is False:
                batteries.disconnect_all()
                return False
        return True

    def construct_grid(self, batteries):
        for battery in batteries.get_members():
            for house in battery.houses.values():
                wire_id = tuple((house.id, battery.id))
                wire = self.generate_wire(wire_id, house, battery)
                self.wires[wire_id] = wire
                house.wire = wire

    def generate_wire(self, wire_id, house, battery) -> Type[Wire]:
        if self.path_type == 'hor_ver':
            wire_path = hor_vert_pathfinder(house.position,
                                            battery.position)
        elif self.path_type == 'straight':
            wire_path = straight_pathfinder(house.position,
                                            battery.position)
        # Make new wire
        wire = Wire(wire_id, house, battery, wire_path)
        return wire

    def connect(self, house, battery) -> None:
        house.connect(battery)
        battery.connect(house)

    def get_paths(self) -> List[List[Coordinate]]:
        colored_paths = [(wire.battery.id, wire.path) for wire in self.wires.values()]
        return colored_paths

    def swap(self, house_1, house_2) -> Dict[int, Type[Wire]]:
        '''Swap to wires'''
        if house_1.id == house_2.id:
            return False

        battery_1 = house_1.battery
        battery_2 = house_2.battery

        if battery_1.can_connect(house_1.max_output - house_2.max_output) is False:
            return False

        if battery_2.can_connect(house_2.max_output - house_1.max_output) is False:
            return False

        battery_1.total_input -= house_1.max_output
        battery_2.total_input -= house_2.max_output

        h1_b2_wire = self.generate_wire((house_1.id, battery_2.id), house_1, battery_2)
        h2_b1_wire = self.generate_wire((house_2.id, battery_1.id), house_2, battery_1)

        self.wires.pop((house_1.id, battery_1.id))
        self.wires.pop((house_2.id, battery_2.id))
        self.wires[h1_b2_wire.id] = h1_b2_wire
        self.wires[h2_b1_wire.id] = h2_b1_wire

        house_1.battery = battery_2
        house_2.battery = battery_1

        if battery_1.id != battery_2.id:
            battery_1.houses.pop(str(house_1.id))
            battery_1.connect(house_2)
            battery_2.houses.pop(str(house_2.id))
            battery_2.connect(house_1)

        return self.wires

    def share_wires(self, dict_wire):
        '''Makes shared wires by making a set of excisting wires that are connected to the same battery'''
        id = 0
        shared_wires = {}
        # Loop over all the wires
        for index, wire in dict_wire.items():
            count = 0
            if index == 0:
                # Make a shared wire
                shared = Shared_wire(wire.house, wire.battery, wire.path)
                shared_wires[id] = shared
                id += 1
                count += 1
            else:
                # Add to excisting wire
                path = set(wire.path)
                for index_share, shared_wire in shared_wires.items():
                    if wire.battery == shared_wire.battery and len(shared_wire.path & path) >= 2:
                        shared_wire.path = shared_wire.path.union(path)
                        shared_wire.house_list.append(wire.house)
                        count = 1
            if count == 0:
                shared = Shared_wire(wire.house, wire.battery, wire.path)
                shared_wires[id] = shared
                id += 1

        return shared_wires
