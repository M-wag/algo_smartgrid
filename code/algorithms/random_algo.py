from ..classes.houses import Houses
from ..classes.batteries import Batteries
from ..classes.wires import Wires
from .calculator import calculate_shared_cost
from copy import deepcopy

def random_algo(iterations, wires, batteries, houses):
    lowest_cost = 9999999
    cost_record = []
    for i in range(iterations):
        houses.disconnect_all()
        batteries.disconnect_all()
        wires.wires.clear()

        grid = False
        while grid == False:
            grid = wires.generate(houses, batteries)

        wires.shared_wires = wires.share_wires(wires.wires)
        cost = calculate_shared_cost(wires.shared_wires, batteries)
        cost_record.append(cost)
        if lowest_cost > cost:
            lowest_cost = cost
            lowest_wires = deepcopy(wires)
        print(f"iteration: {i}, cost: {cost}")

    return lowest_cost, lowest_wires, cost_record