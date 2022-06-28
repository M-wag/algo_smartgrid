from typing import Type, Tuple, List, Dict
class Wire:
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

    def __init__(self, id: int, house, battery,
                 path: List[Tuple[int, int]]) -> None:
        self.id = id
        self.house = house
        self.battery = battery
        self.path = path

class Shared_wire:
    """
    A class to represent a shared wire.

    ...

    Attributes
    ----------
    id : int
        the wires id
    house_list: List[House]
        a list of all the houses connect to this shared wire
    battery : Type[Battery]
        the Battery object connected to the shared wire
    path : Set[Tuple[int, int]]
        a set of unique coordinates along which the wire is laid
    """

    def __init__(self, house, battery, path):
        self.house_list = []
        self.house_list.append(house)
        self.battery = battery
        self.path = set(path)