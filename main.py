import argparse
import json
from classes.houses import Houses
from classes.batteries import Batteries
from classes.wires import Wires
from visualize import visualize_grid, visualize_bar, visualize_hill
from algorithms.hillclimber import hillclimber
from algorithms.simulated_annealing import simulated_annealing
from algorithms.random_algo import random_algo

max_restart_boundary = 2500
max_iterations = 100000

def main(algorithm, wijk_num: str, iterations: int, restart_hillclimber, file_name) -> None:

    houses = Houses(f'data/district_{wijk_num}/district-{wijk_num}_houses.csv')             # noqa: E501
    batteries = Batteries(f'data/district_{wijk_num}/district-{wijk_num}_batteries.csv')    # noqa: E501
    wires = Wires()

    if algorithm == 'hillclimber':
        lowest_cost, lowest_wires, cost_record = hillclimber(iterations, restart_hillclimber, wires, batteries, houses)
        visualize_hill(cost_record, f'output/wijk_{wijk_num}_hill_{file_name}.png')
    elif algorithm == 'random':
        lowest_cost, lowest_wires, cost_record = random_algo(iterations, wires ,batteries, houses)
        visualize_bar(cost_record, f'output/wijk_{wijk_num}_bar_{file_name}.png')
    elif algorithm == 'simulated_annealing':
         lowest_cost, lowest_wires, cost_record = simulated_annealing(iterations, 30, wires, batteries, houses)
         visualize_hill(cost_record, f'output/wijk_{wijk_num}_hill_{file_name}.png')

    # Save Grid Plot
    visualize_grid(houses.get_members(),
    batteries.get_members(),
    lowest_wires.get_paths(), f'output/wijk_{wijk_num}_smartgrid_{file_name}.png')

    # Save JSON
    dict_json = {"district" : wijk_num, "shared-costs" : lowest_cost}
    json_object = json.dumps(dict_json, indent = 2)
    with open(f'output/wijk_{wijk_num}_smartgrid_{file_name}.json', "w") as outfile:
        outfile.write(json_object)
    
def get_positive_int(input_text, upper_limit):
    """
    Get a postive integer through user input, under a certain limit.

    Parameters
    ----------
    input_text: str
        Text showcased in terminal
    upper_limit : int
        Upper boundary of positive integers
    """
    while True:
        try:
            pos_int = int(input(input_text))
        except ValueError:
            print('Please pass a integer')
            continue
        if pos_int <= 0:
            print('Make sure the integer is positive')
            continue
        if pos_int > upper_limit:
            print('Passed integer exceeds the upper limit')
            continue
        return pos_int

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=(
                "Generates a SmartGrid for input houses and batteries"))

    # Adding arguments
    parser.add_argument("algorithm",
                        help="wijk number)")

    # Read arguments from command line
    args = parser.parse_args()

    wijk = get_positive_int('Select neighborhoud:', 3) 
    iterations = get_positive_int('Iteration amount:', max_iterations)
    file_name = input('File name:')

    if args.algorithm == 'hillclimber':
        hill_restart = get_positive_int('Restart boundary for hill climber:', max_restart_boundary)
    elif args.algorithm == 'simulated_annealing':
        hill_restart = 1
    elif args.algorithm == "random":
        hill_restart = 1
    else:
        print('No valid argument passed')
        
    # Run our line function with provided arguments
    main(args.algorithm, wijk, iterations, hill_restart, file_name)


