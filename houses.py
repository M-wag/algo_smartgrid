import pandas as pd
import random
from typing import Dict, Tuple, Type, List
from batteries import Battery


class House():
    """
    A class to represent a house.

    ...

    Attributes
    ----------
    position : Tuple[int, int]
        x and y coordinates of the house
    max_output : float
        maximum energy output of the house
    battery : Type[Battery]
        battery object connected to the house
    wire : Type[Wire]
        wire object connected to the house and its battery

    Methods
    -------
    assign_wire(self, wire) -> None:
        assigns a Wire object to the house
    connect(self, house: Type[House]) -> None:
        assigns a Battery object to the house
    """

    def __init__(self, position: Tuple[int, int], max_output: float, container) -> None:
        self.position = position
        self.max_output = max_output
        self.battery = None
        self.wire = None
        self.container = container

    # assign wire to house
    def assign_wire(self, wire) -> None:
        self.wire = wire

    def connect(self, battery: Type[Battery]) -> None:
        self.battery = battery
        self.container.add_connected_house(self)


class Houses():
    """
    A class to represent a collection of houses.

    ...

    Attributes
    ----------
    dict_houses : Dict[int, Type[House]]
        a dictionary with all House objects contained
    order : List[int]
        the order in which to iterate over the dictionary
    connected_houses : List[House]    
        a list of all House objects connected to a battery

    Methods
    -------
    load(self, Houses_csv: str) -> Dict[int, Type[House]]:
        loads the csv-file data into House classes and adds them to a dict
    shuffle_order(self) -> List[int]:
        shuffles the order of items in the order list
    get_members(self) -> Tuple[int, Type[House]]:
        returns all House objects together with their keys
    get_member_coords(self) -> List[Tuple[int, int]]:
        returns a list of all House positions
    all_houses_connected(self) -> bool:
        returns whether all houses are connected to a battery
    """

    def __init__(self, houses_csv: str) -> None:
        self.dict_houses = {}
        self.order = None
        self.connected_houses = []
        self.load(houses_csv)

    # Load houses from csv_file into dictionary, called upon init
    def load(self, houses_csv: str) -> Dict[int, Type[House]]:
        df_houses = pd.read_csv(houses_csv)

        for id, row in df_houses.iterrows():
            position = (int(row['x']), int(row['y']))
            max_output = float(row['maxoutput'])
            self.dict_houses[id] = House(position, max_output, self)
            self.order = list(self.dict_houses.keys())

        return self.dict_houses

    def shuffle_order(self):
        random.shuffle(self.order)
        return self.order

    def get_members(self):
        return self.dict_houses.values()

    def get_member_coords(self) -> List[Tuple[int, int]]:
        member_coords = [house.position for house in self.dict_houses.values()]
        return member_coords

    def add_connected_house(self, house) -> None:
        self.connected_houses.append(house)

    def all_houses_connected(self):
        if len(self.connected_houses) == len(self.dict_houses):
            return True
        return False
