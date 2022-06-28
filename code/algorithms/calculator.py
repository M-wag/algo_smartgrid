# takes in the amount of wire used and batteries used, and calculates the cost
from typing import Type
from code.classes.batteries import Batteries
from code.classes.houses import Houses

def calculate_own_cost(houses: Type[Houses],
                       batteries: Type[Batteries]) -> float:
    '''
    Returns the total cost of the SmartGrid when cannot be shared

            Parameters:
                    houses (Houses):
                        A class containing House objects
                    batteries (Batteries):
                        A class containing Batteries objects

            Returns:
                    Total cost (float):
                         The total cost of the SmartGrid
    '''

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

    total_cost = total_wire * 9 + total_batteries * 5000
    return total_cost


def calculate_shared_cost(shared_wires: dict,
                          batteries: Type[Batteries]) -> float:
    '''
    Returns the total cost of the SmartGrid when wires can be shared

            Parameters:
                    wires (Wires):
                        A class containing Wire objects
                    batteries (Batteries):
                        A class containing Batteries objects

            Returns:
                    Total cost (float):
                         The total cost of the SmartGrid
    '''

    total_wire = 0
    for wire_branch in shared_wires.values():
        total_wire += len(wire_branch.path) - 1

    total_batteries = 0
    for battery in batteries.get_members():
        total_batteries += 1

    total_cost = total_wire * 9 + total_batteries * 5000
    return total_cost


def calculate_cluster_cost(wire_branches, batteries):
    total_cost = 0
    for branch in wire_branches:
        total_cost += (len(branch) - 1) * 9
    total_cost += len(batteries.get_members()) * 5000

    return total_cost
