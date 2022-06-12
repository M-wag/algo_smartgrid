# class wire & class wires met make functie
from typing import List, Tuple, Type
from houses import House
from batteries import Battery


class Wire:

    def __init__(self, list_coor: List[Tuple[int, int]]) -> None:
        self.list_coor = list_coor


class Wires:

    def __init__(self) -> None:
        self.dict_wires = {}
        self.wire_id = 0

    def make_wire(self, battery: Type[Battery], house: Type[House]) -> None:
        wire_points = []
        battery_x, battery_y = battery.position
        house_x, house_y = house.position

        wire_x, wire_y = battery_x, battery_y

        x_dif = house_x - battery_x
        y_dif = house_y - battery_y

        if x_dif == 0:
            x_direction = 0
        else:
            x_direction = int(x_dif / abs(x_dif))
        if y_dif == 0:
            y_direction = 0
        else:
            y_direction = int(y_dif / abs(y_dif))

        wire_points.append((wire_x, wire_y))
        while house_x != (wire_x + x_direction):
            wire_x += x_direction
            wire_points.append((wire_x, wire_y))

        while house_y != (wire_y + y_direction):
            wire_y += y_direction
            wire_points.append((wire_x, wire_y))

        self.dict_wires[self.wire_id] = Wire(wire_points)
        self.wire_id += 1
