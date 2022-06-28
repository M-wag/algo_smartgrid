import pandas as pd
import random
from typing import Tuple, Type, List, Dict


class Battery:
    """
    A class to represent a Battery.

    ...

    Attributes
    ----------
    position : Tuple[int, int]
        x and y coordinates of the battery
    capacity : float
        total capacity of the battery
    total_input : float
        total accumulated output from houses
    houses : List[Type[House]]
        list of all connected houses

    Methods
    -------
    can_connect(house_output: float) -> bool:
        returns whether or not a house can connect
    connect(self, house: Type[House]) -> None:
        adds the house to the "houses" list and calculates the total_input
    """

    def __init__(self, id: int, position: Tuple[int, int], capacity: float) -> None:
        self.id = id
        self.position = position
        self.capacity = capacity
        self.total_input = 0
        self.houses = {}

    def can_connect(self, house_output: float) -> bool:
        if self.total_input + house_output > self.capacity:
            return False
        return True

    def connect(self, house) -> None:
        self.houses[str(house.id)] = house
        self.total_input += house.max_output
    
    def disconnect(self, house) -> None:
        self.houses.pop(str(house.id))
        self.total_input -= house.max_output


class Batteries:
    """
    A class to represent a collection of batteries.

    ...

    Attributes
    ----------
    dict_batteries : Dict[int, Type[Battery]]
        a dictionary with all Battery objects contained
    order : List[int]
        the order in which to iterate over the dictionary

    Methods
    -------
    load(self, batteries_csv: str) -> Dict[int, Type[Battery]]:
        loads the csv-file data into Battery classes and adds them to a dict
    shuffle_order(self) -> List[int]:
        shuffles the order of items in the order list
    get_members(self) -> Tuple[int, Type[Battery]]:
        returns all Battery objects together with their keys
    get_member_coords(self) -> List[Tuple[int, int]]:
        returns a list of all Battery positions
    """

    def __init__(self, batteries_csv: str) -> None:
        self.dict_batteries = {}
        self.order = None
        self.load(batteries_csv)

    def load(self, batteries_csv: str) -> Dict[int, Type[Battery]]:
        df_batteries = pd.read_csv(batteries_csv)

        for id, row in df_batteries.iterrows():
            x, y = row['positie'].split(',')
            capacity = int(row['capaciteit'])
            self.dict_batteries[id] = Battery(id, (int(x), int(y)), capacity)
            self.order = list(self.dict_batteries.keys())

        return self.dict_batteries

    def shuffle_order(self) -> List[int]:
        random.shuffle(self.order)
        return self.order

    def get_members(self) -> Tuple[int, Type[Battery]]:
        return self.dict_batteries.values()

    # def get_member_coords(self) -> List[Tuple[int, int]]:
    #     member_coords = [battery.position for battery in
    #                      self.dict_batteries.values()]
    #     return member_coords
    
    def disconnect_all(self):
        for battery in self.dict_batteries.values():
            battery.houses = {}
            battery.total_input = 0
