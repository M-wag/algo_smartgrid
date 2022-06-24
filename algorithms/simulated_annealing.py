from classes.houses import Houses
from classes.batteries import Batteries
from classes.wires import Wires
from calculator import calculate_shared_cost
import random


def simulated_annealing(iterations, temperature, wires, batteries, houses):
    # initialise a grid
    grid = False
    while grid == False:
        grid = wires.generate(houses, batteries)
    
    # calculate the cost
    wires.shared_wires = wires.share_wires(wires.wires)
    cost = calculate_shared_cost(wires.shared_wires, batteries)

    # initialise the temperature
    t = temperature

    cost_record = [cost]
    for i in range(iterations):
        print(f"iteration: {i}, cost: {cost}")
        # swap two houses until a valid solution has been found
        swapped = False
        while swapped == False:
            house_1, house_2 = 1, 1
            while house_1 == house_2:
                house_1 = houses.random_pick()
                house_2 = houses.random_pick()
            swapped = wires.swap(house_1, house_2)
        new_grid, new_house_1, new_house_2, new_battery_1, new_battery_2 = swapped
        
        # calculate new cost
        new_wire_set = wires.share_wires(new_grid)
        new_cost = calculate_shared_cost(new_wire_set, batteries)

        # always accept better solutions
        if new_cost < cost:
            cost = new_cost
            wires.wires = new_grid
            wires.shared_wires = new_wire_set
            houses.dict_houses[new_house_1.id] = new_house_1
            houses.dict_houses[new_house_2.id] = new_house_2
            batteries.dict_batteries[new_battery_1.id] = new_battery_1
            batteries.dict_batteries[new_battery_2.id] = new_battery_2

        else:

            # calculate the acceptance chance and generate a random number
            random_nr = random.random()
            r_acceptance = 2 ** ((cost - new_cost) / t)

            # if the random number is lower, accept the changes
            if random_nr < r_acceptance:
                cost = new_cost
                wires.wires = new_grid
                wires.shared_wires = new_wire_set
                houses.dict_houses[new_house_1.id] = new_house_1
                houses.dict_houses[new_house_2.id] = new_house_2
                batteries.dict_batteries[new_battery_1.id] = new_battery_1
                batteries.dict_batteries[new_battery_2.id] = new_battery_2

        # lower the temperature after every iteration
        t = temperature - (temperature / iterations) * i
        cost_record.append(cost)

    return cost, wires, cost_record
