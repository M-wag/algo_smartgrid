from typing import Type, Tuple, List
from code.classes.houses import Houses
from code.classes.batteries import Batteries
from code.classes.wires import Wires
from code.algorithms.calculator import calculate_shared_cost
from copy import deepcopy


def begin_state(wires: Type[Wires], batteries: Type[Batteries], houses: Type[Houses]):
    '''
    Creates a random begin grid and calculates the cost of that grid
            Parameters:
                    wires (Wires):
                        A class representing all the wires
                    Batteries (Battery):
                        A class representing all batteries
                    Houses (House):
                        A class representing all houses

            Returns:
                    The cost of the grid
    '''
    grid = False
    # Generate a random grid till a valid grid is found
    while grid is False:
        # Generate a grid
        grid = wires.generate(houses, batteries)
    # Make wires
    wires.construct_grid(batteries)
    # Make shared wires for swapped
    wires.shared_wires = wires.share_wires(wires.wires)
    # Calculate cost
    cost = calculate_shared_cost(wires.shared_wires, batteries)
    return cost


def swap_and_cost(wires: Type[Wires], batteries: Type[Batteries], houses: Type[Houses]):
    '''
    Swaps two houses in de grid and calculates the cost of the new_grid
            Parameters:
                    wires (Wires):
                        A class representing all the wires
                    Batteries (Battery):
                        A class representing all batteries
                    Houses (House):
                        A class representing all houses

            Returns:
                    The cost of the new grid
    '''
    swapped = False
    # Swap till you find a valid swap
    while swapped is False:
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


def hillclimber(iterations: int,
                restart: int,
                wires: Type[Wires],
                batteries: Type[Batteries],
                houses: Type[Houses]) -> Tuple[List[int], Type[Wires], int]:
    '''
    Function to run the hillclimber algorithm
            Parameters:
                    Iterations:
                        Number of times the hillclimber algorithm is run
                    Restart:
                        After how many consecutive times no better grid is found the algorithm should restart
                    Wires (Wires):
                        A class representing all the wires
                    Batteries (Battery):
                        A class representing all batteries
                    Houses (House):
                        A class representing all houses

            Returns:
                    The lowest cost, the wires and batteries associated with this cost and a list of all the costs
    '''
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
