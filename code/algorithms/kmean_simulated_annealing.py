import random
from sklearn import metrics
from .kmean_cluster_functions import cluster_swap, pick_and_swap, generate_clusters  # noqa: E501
from .calculator import calculate_shared_cost


def random_begin_state(wires, batteries, houses, type_wires):
    '''
    Divides the houses randomly over the batteries,
    until a valid division has been found

            Parameters:
                    wires (Wires):
                        A class containing wire objects
                    batteries (Batteries):
                        A class containing Battery objects
                    houses (Houses):
                        A class containing House objects
                    type_wires ("string"):
                        The wire pathfinding type

            Returns:
                    cost (float):
                         The total cost of the SmartGrid
    '''

    grid = False
    # Generate a random grid till a valid grid is found
    while grid is False:
        grid = wires.generate(houses, batteries)

    # generate the clusters
    generate_clusters(batteries, wires, type_wires)

    # generate the shared wires
    shared_wires = wires.share_wires(wires.wires)

    # calculate the cost of the current setup
    cost = calculate_shared_cost(shared_wires, batteries)

    return cost


def simulated_annealing_begin_state(iterations, temperature, wires,
                                    batteries, houses, type_wires):
    '''
    Divides the houses randomly over the batteries,
    then uses simulated annealing to find a grid with the lowest
    silhouette-score

            Parameters:
                    iterations (int):
                        The amount of iterations
                    temperature (int):
                        The starting temperature
                    wires (Wires):
                        A class containing wire objects
                    batteries (Batteries):
                        A class containing Battery objects
                    houses (Houses):
                        A class containing House objects
                    type_wires (str):
                        A string with the chosen Wire path finding

            Returns:
                    cost (int):
                        The total cost of the current setup
                    score_record (List[int]):
                        A list of all recorded "best_score" values
    '''

    grid = False
    # Generate a random grid till a valid grid is found
    while grid is False:
        grid = wires.generate(houses, batteries)

    best_score = -1
    score_record = []
    t = temperature
    for i in range(iterations):

        # swap two houses until a valid setup has been found
        battery_1, house_1, battery_2, house_2 = pick_and_swap(batteries)

        # generate lists for all house coordinates and their respective cluster
        all_houses = []
        all_house_labels = []
        for battery in batteries.get_members():
            battery_houses = [house.position
                              for house in battery.houses.values()]
            all_houses += battery_houses

            all_house_labels += [battery.id
                                 for house in battery.houses.values()]

        # calculate the silhouette-score for the current setup
        silhou_score = metrics.silhouette_score(all_houses,
                                                all_house_labels,
                                                metric='euclidean')

        # always accept better solutions
        if silhou_score > best_score:
            best_score = silhou_score

        else:

            # calculate the acceptance chance and generate a random number
            random_nr = random.random()
            try:
                # 60000 chosen to normalize a good temp choice around 100
                r_acceptance = 2 ** (((silhou_score - best_score) * 60000) / t)

            # as the r_acceptance lowers, the float will become too long
            except OverflowError:
                r_acceptance = 0

            # if the random number is lower, accept the changes
            if random_nr < r_acceptance:
                best_score = silhou_score

            # otherwise, revert the change
            else:
                cluster_swap(battery_1, house_2, battery_2, house_1)

        # lower the temperature after every iteration
        t = temperature - (temperature / iterations) * i

        # add the current best score to the score record
        score_record.append(best_score)

    # generate the clusters
    generate_clusters(batteries, wires, type_wires)

    # generate the shared wires
    shared_wires = wires.share_wires(wires.wires)

    # calculate the cost of the current setup
    cost = calculate_shared_cost(shared_wires, batteries)

    return cost, score_record


def kmean_simulated_annealing(iterations, temperature, wires, batteries,
                              houses, begin_state, type_wires,
                              score_temperature):
    '''
    Uses simulated annealing to find a setup with the lowest possible cost

            Parameters:
                    iterations (int):
                        The amount of iterations
                    temperature (int):
                        The starting temperature
                    wires (Wires):
                        A class containing Wire objects
                    batteries (Batteries):
                        A class containing Battery objects
                    houses (Houses):
                        A class containing House objects
                    begin_state (string):
                        the chosen begin state of the grid
                    type_wires (str):
                        A string with the chosen Wire path finding

            Returns:
                    cost (int):
                        The total cost of the current setup
                    wires (Wires):
                        A class containing Wire objects
                    batteries (Batteries):
                        A class containing Battery objects
                    cost_record (List[int]):
                        A list of all recorded cost values
                    score_record (List[int]):
                        A list of all recorded silhouette-score values
    '''

    # initialise a grid
    if begin_state == "simulated_annealing":
        cost, score_record = simulated_annealing_begin_state(1000, score_temperature,  # noqa: E501
                                                             wires, batteries,
                                                             houses,
                                                             type_wires)
    else:
        cost = random_begin_state(wires, batteries, houses, type_wires)
        score_record = []

    # initialise the temperature
    t = temperature

    cost_record = [cost]
    for i in range(iterations):
        # swap two houses until a valid setup has been found
        battery_1, house_1, battery_2, house_2 = pick_and_swap(batteries)

        # generate the wire branches and individual wire-paths
        generate_clusters(batteries, wires, type_wires)

        # generate the shared wires
        shared_wires = wires.share_wires(wires.wires)

        # calculate the new cost of the setup
        new_cost = calculate_shared_cost(shared_wires, batteries)

        # always accept better solutions
        if new_cost < cost:
            cost = new_cost

        else:

            # calculate the acceptance chance and generate a random number
            random_nr = random.random()
            try:
                r_acceptance = 2 ** ((cost - new_cost) / t)

            # as the r_acceptance lowers, the float will become too long
            except OverflowError:
                r_acceptance = 0

            # if the random number is lower, accept the changes
            if random_nr < r_acceptance:
                cost = new_cost

            # otherwise, revert the change
            else:
                cluster_swap(battery_1, house_2, battery_2, house_1)

        # lower the temperature after every iteration
        t = temperature - (temperature / iterations) * i

        # add the cost to the cost record
        cost_record.append(cost)

    return cost, wires, batteries, cost_record, score_record
