import argparse
import json
from classes.houses import Houses
from classes.batteries import Batteries
from classes.wires import Wires
from visualize import visualize_grid, visualize_bar, visualize_hill
from algorithms.hillclimber import hillclimber
from algorithms.simulated_annealing import simulated_annealing
from algorithms.random_algo import random_algo


def main(algorithm, wijk_num: str, iterations: int, restart_hillclimber, file_name) -> None:

    houses = Houses(f'data/district_{wijk_num}/district-{wijk_num}_houses.csv')             # noqa: E501
    batteries = Batteries(f'data/district_{wijk_num}/district-{wijk_num}_batteries.csv')    # noqa: E501
    wires = Wires()

    if algorithm == 'hillclimber':
        lowest_cost, lowest_wires, cost_record = hillclimber(iterations, restart_hillclimber, wires, batteries, houses)
        visualize_hill(cost_record, f'output/wijk_{wijk_num}_hill_{file_name}.png')
    elif algorithm == 'random':
        lowest_cost, lowest_wires = random_algo(iterations, wires ,batteries, houses)
        visualize_bar(cost_record, f'output/wijk_{wijk_num}_bar_{file_name}.png')
    elif algorithm == 'simulated_annealing':
         lowest_cost, lowest_wires, cost_record = simulated_annealing(iterations, 100, wires, batteries, houses)
         visualize_hill(cost_record, f'output/wijk_{wijk_num}_hill_{file_name}.png')

    # Plot grid and save
    visualize_grid(houses.get_member_coords(),
    batteries.get_member_coords(),
    lowest_wires.get_paths(), f'output/wijk_{wijk_num}_smartgrid_{file_name}.png')

    dict_json = {"district" : wijk_num, "shared-costs" : lowest_cost}
    json_object = json.dumps(dict_json, indent = 2)
    with open(f'output/wijk_{wijk_num}_smartgrid_{file_name}.json', "w") as outfile:
        outfile.write(json_object)
    
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=(
                "Generates a SmartGrid for input houses and batteries"))

    # Adding arguments
    parser.add_argument("algorithm",
                        help="wijk number)")
    parser.add_argument("wijk",
                        help="wijk number)")
    parser.add_argument("iterations",
                        help="number of iterations", type=int)
    parser.add_argument("restart",
                        help="number of iterations", type=int)
    parser.add_argument("file_name",
                        help="number of runs")

    # Read arguments from command line
    args = parser.parse_args()

    # Run our line function with provided arguments
    main(args.algorithm, args.wijk, args.iterations, args.restart, args.file_name)
