from classes.houses import Houses
from classes.batteries import Batteries
from classes.wires import Wires
from calculator import calculate_shared_cost
import random


def simulated_annealing(iterations, temperature, delta_t, wires, batteries, houses):
    lowest_cost = 9999999
    cost_record = []
    # initialise a grid
    grid = False
    while grid == False:
        grid = wires.generate(houses, batteries)
    
    # calculate the cost
    wires.shared_wires = wires.share_wires(wires.wires)
    cost = calculate_shared_cost(wires.shared_wires, batteries)

    # initialise the temperature
    t = temperature

    for i in range(iterations):

        # swap two houses until a valid solution has been found
        new_grid = False
        while new_grid == False:
            house_1 = houses.random_pick()
            house_2 = houses.random_pick()
            new_grid = wires.swap(house_1, house_2)
        
        # calculate new cost
        new_wire_set = wires.share_wires(new_grid)
        new_cost = calculate_shared_cost(new_wire_set, batteries)

        # always accept better solutions
        if new_cost < cost:
            cost = new_cost
            wires.wires = new_grid
            wires.shared_wires = new_wire_set

        else:

            # calculate the acceptance chance and generate a random number
            random_nr = random.random()
            r_acceptance = 2 ** ((cost - new_cost) / temperature)

            # if the random number is lower, accept the changes
            if random_nr < r_acceptance:
                cost = new_cost
                wires.wires = new_grid
                wires.shared_wires = new_wire_set
        
        # lower the temperature after every iteration
        t -= delta_t
        cost_record.append(cost)
        if cost < lowest_cost:
            lowest_cost = cost
            lowest_wires = deepcopy(wires)

    return lowest_cost, lowest_wires, cost_record

if __name__ == "__main__":
    pass