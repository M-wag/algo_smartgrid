from classes.houses import Houses
from classes.batteries import Batteries
from classes.wires import Wires
from .hillclimber import begin_state
from copy import deepcopy

def random_algo(iterations, wires, batteries, houses):
    lowest_cost = 9999999
    cost_record = []
    for i in range(iterations):
        houses.disconnect_all()
        batteries.disconnect_all()
        wires.wires.clear()
        cost = begin_state(wires, batteries, houses)
        cost_record.append(cost)
        if lowest_cost > cost:
            lowest_cost = cost
            lowest_wires = deepcopy(wires)
        print(f"iteration: {i}, cost: {cost}")

    return lowest_cost, lowest_wires, cost_record