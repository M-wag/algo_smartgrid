from houses import Houses, House
from batteries import Batteries, Battery
from typing import Type, Tuple, List
from path_finders import random_path_finder


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
                 path: List[Tuple[int, int]], container) -> None:
        self.id = id
        self.house = house
        self.battery = battery
        self.path = path
        self.container = container


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
        self.wire_segments = set()

    def generate(self, houses: Type[Houses],
                 batteries: Type[Batteries]) -> bool:

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
                    wire_path = random_path_finder(house_coord,
                                                   battery_coord,
                                                   self.wire_segments)
                    # Make new wire
                    wire = Wire(wire_id, house, battery, wire_path)
                    self.wires[wire_id] = wire
                    wire_id += 1
                    has_battery = True
                    break

            if has_battery is False:
                return False
        return True

    def total_wires_segments(self) -> int:
        return len(self.wire_segments)

    def connect(self, house: Type[House], battery: Type[Battery]) -> None:
        house.connect(battery)
        battery.connect(house)

    def get_paths(self) -> List[List[Tuple[int, int]]]:
        paths = [wire.path for wire in self.wires.values()]
        return paths
