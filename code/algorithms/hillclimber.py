from code.classes.houses import Houses
from code.classes.batteries import Batteries
from code.classes.wires import Wires
from code.algorithms.calculator import calculate_shared_cost
from copy import deepcopy

def begin_state(wires, batteries, houses):
    grid = False
    # Generate a random grid till a valid grid is found
    while grid == False:
        # Generate a grid
        grid = wires.generate(houses, batteries)
    # Make wires
    wires.construct_grid(batteries)
    # Make shared wires for swapped
    wires.shared_wires = wires.share_wires(wires.wires)
    # Calculate cost
    cost = calculate_shared_cost(wires.shared_wires, batteries)
    return cost

def swap_and_cost(wires, batteries, houses):
    swapped = False
    # Swap till you find a valid swap
    while swapped == False:
        # Pick a two random houses
        house_1 = houses.random_pick()
        house_2 = houses.random_pick()
        # Swap the wires
        swapped = wires.swap(house_1, house_2)
    
    new_grid = swapped
    # Make shared wires for swapped
    new_shared_wires = wires.share_wires(new_grid)
    # Calculate cost   
    new_cost = calculate_shared_cost(new_shared_wires, batteries)
    return house_1, house_2, new_cost

def hillclimber(iterations: int, restart, wires, batteries, houses):
    cost_record = []
    count = 0
    lowest_cost = 99999999
    # Make a begin grid
    cost = begin_state(wires, batteries, houses)
    cost_record.append(cost)
    # Iterate
    for i in range(iterations):
        count += 1
        # Do a swap
        house_1, house_2, new_cost = swap_and_cost(wires, batteries, houses)
        print(f"iteration {i}, lowest_ cost {lowest_cost}, cost {cost}, new_cost {new_cost}, count {count}")
        if new_cost < cost:
            cost = new_cost
            count = 0
        else:
            # Swap back
            wires.swap(house_1, house_2)
        # If the value for the restart is reached
        if count > restart:
            houses.disconnect_all()
            batteries.disconnect_all()
            cost = begin_state(wires, batteries, houses)
            count = 0
        cost_record.append(cost)
        # Save the lowest
        if lowest_cost > cost:
            lowest_cost = cost
            lowest_wires = deepcopy(wires)
            lowest_batteries = deepcopy(batteries)
    
    return lowest_cost, lowest_wires, lowest_batteries, cost_record