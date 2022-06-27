from classes.houses import Houses
from classes.batteries import Batteries
from classes.wires import Wires
from algorithms.calculator import calculate_shared_cost
from copy import deepcopy

def begin_state(wires, batteries, houses):
    grid = False
    while grid == False:
        grid = wires.generate(houses, batteries)
    wires.shared_wires = wires.share_wires(wires.wires)
    cost = calculate_shared_cost(wires.shared_wires, batteries)
    return cost

def swap_and_cost(wires, batteries, houses):
    swapped = False
    while swapped == False:
        house_1 = houses.random_pick()
        house_2 = houses.random_pick()
        swapped = wires.swap(house_1, house_2)
    new_grid = swapped
    new_shared_wires = wires.share_wires(new_grid)
        
    new_cost = calculate_shared_cost(new_shared_wires, batteries)
    return house_1, house_2, new_cost

def hillclimber(iterations: int, restart, wires, batteries, houses):
    cost_record = []
    count = 0
    lowest_cost = 99999999
    cost = begin_state(wires, batteries, houses)
    cost_record.append(cost)
    for i in range(iterations):
        count += 1
        house_1, house_2, new_cost = swap_and_cost(wires, batteries, houses)
        print(f"iteration {i}, lowest_ cost {lowest_cost}, cost {cost}, new_cost {new_cost}, count {count}")
        if new_cost < cost:
            cost = new_cost
            count = 0
        else:
            wires.swap(house_1, house_2)
        
        if count > restart:
            houses.disconnect_all()
            batteries.disconnect_all()
            cost = begin_state(wires, batteries, houses)
            count = 0
        cost_record.append(cost)
        if lowest_cost > cost:
            lowest_cost = cost
            lowest_wires = deepcopy(wires)
    
    return lowest_cost, lowest_wires, cost_record