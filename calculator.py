# takes in the amount of wire used and batteries used, and calculates the cost
from typing import Type
from batteries import Batteries
from houses import Houses


def calculate_cost(houses: Type[Houses], batteries: Type[Batteries]) -> float:
    total_wire = 0
    for house in houses.get_members():
        house_x, house_y = house.position
        battery_x, battery_y = house.battery.position

        # manhattan distance
        wire_length = abs(house_x - battery_x) + abs(house_y - battery_y)
        total_wire += wire_length

    total_batteries = 0
    for battery in batteries.get_members():
        total_batteries += 1

    return total_wire * 9 + total_batteries * 5000
