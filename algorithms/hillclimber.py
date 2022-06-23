from classes.houses import Houses
from classes.batteries import Batteries
from classes.wires import Wires
from calculator import calculate_shared_cost
from copy import deepcopy

def hillclimber(iterations: int,  restart, wires, batteries, houses):
    cost_record = []
    count = 0
    lowest_cost = 99999999
    grid = False
    while grid == False:
        grid = wires.generate(houses, batteries)
    wires.shared_wires = wires.share_wires(wires.wires)
    cost = calculate_shared_cost(wires.shared_wires, batteries)
    cost_record.append(cost)
    for i in range(iterations):
        count += 1
        new_wires = False
        while new_wires == False:
            house_1 = houses.random_pick()
            house_2 = houses.random_pick()
            new_wires = wires.swap(house_1, house_2)
        new_shared_wires = wires.share_wires(new_wires)
        new_cost = calculate_shared_cost(new_shared_wires, batteries)
        print(f"iteration {i}, lowest_ cost {lowest_cost}, cost {cost}, new_cost {new_cost}, count {count}")
        if new_cost < cost:
            cost = new_cost
            wires.wires = new_wires
            wires.shared_wires = new_shared_wires
            count = 0
        
        if count > restart:
            houses.disconnect_all()
            batteries.disconnect_all()
            grid = False
            while grid == False:
                grid = wires.generate(houses, batteries)
            wires.shared_wires = wires.share_wires(wires.wires)
            cost = calculate_shared_cost(wires.shared_wires, batteries)
            count = 0
        cost_record.append(cost)
        if lowest_cost > cost:
            lowest_cost = cost
            lowest_wires = deepcopy(wires)
    
    return lowest_cost, lowest_wires, cost_record