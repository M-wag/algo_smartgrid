from code.classes.houses import Houses
from code.classes.batteries import Batteries
from code.classes.wires import Wires
from .hillclimber import begin_state
from copy import deepcopy
from typing import Type


def random_algo(iterations: int,
                wires: Type[Wires],
                batteries: Type[Batteries],
                houses: Type[Houses]):
    '''
    Function to run the random algorithm
            Parameters:
                    Iterations:
                        Number of times the random algorithm is run
                    Wires (Wires):
                        A class representing all the wires
                    Batteries (Battery):
                        A class representing all batteries
                    Houses (House):
                        A class representing all houses

            Returns:
                    The lowest cost, the wires and batteries associated with this cost and a list of all the costs
    '''
    lowest_cost = 9999999
    cost_record = []
    for i in range(iterations):
        # Disconnect all houses and batteries
        houses.disconnect_all()
        batteries.disconnect_all()
        # Delete all wires
        wires.wires.clear()
        # Make a grid and calculate cost
        cost = begin_state(wires, batteries, houses)
        cost_record.append(cost)
        # Save lowest
        if lowest_cost > cost:
            lowest_cost = cost
            lowest_wires = deepcopy(wires)
            lowest_batteries = deepcopy(batteries)

    return lowest_cost, lowest_wires, lowest_batteries, cost_record
