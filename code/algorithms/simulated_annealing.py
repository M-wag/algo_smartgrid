from .hillclimber import begin_state, swap_and_cost
import random


def simulated_annealing(iterations, temperature, wires, batteries, houses):
    # initialise a grid
    cost = begin_state(wires, batteries, houses)
    # initialise the temperature
    t = temperature

    cost_record = [cost]
    for i in range(iterations):
        print(f"iteration: {i}, cost: {cost}")
        # swap two houses until a valid solution has been found
        house_1, house_2, new_cost = swap_and_cost(wires, batteries, houses)

        # always accept better solutions
        if new_cost < cost:
            cost = new_cost

        else:

            # calculate the acceptance chance and generate a random number
            random_nr = random.random()
            try: 
                r_acceptance = 2 ** ((cost - new_cost) / t)
            except OverflowError: 
                r_acceptance = 0

            # if the random number is lower, accept the changes
            if random_nr < r_acceptance:
                cost = new_cost
            
            # otherwise, revert the change
            else:
                wires.swap(house_1, house_2)

        # lower the temperature after every iteration
        t = temperature - (temperature / iterations) * i
        cost_record.append(cost)

    return cost, wires, cost_record
