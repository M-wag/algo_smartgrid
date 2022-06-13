import argparse
import json
from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_cost
from visualize import visualize_grid


def main(wijk_num: str, n: int) -> None:
    lowest_cost = 1000000
    # Generate wires
    for i in range(n):
        # init
        houses = Houses(f'district-{wijk_num}_houses.csv')
        batteries = Batteries(f'district-{wijk_num}_batteries.csv')
        wires = Wires()
        # Make wires 
        if wires.generate(houses, batteries):
            cost = calculate_cost(houses, batteries)
            print(i, cost)
            if cost < lowest_cost:
                lowest_cost = cost
                # Plot grid and save
                visualize_grid(houses.get_member_coords(),
                   batteries.get_member_coords(),
                   wires.get_paths(), f'smartgrid_wijk_{wijk_num}.png')
        else:
            print(i,'No valid outcome')
    
    dict_json = { "district" : wijk_num, "own-costs" : lowest_cost}
    json_object = json.dumps(dict_json, indent = 2)
    with open(f'smartgrid_wijk_{wijk_num}.json', "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=(
                "Generates a SmartGrid for input houses and batteries"))

    # Adding arguments
    parser.add_argument("wijk",
                        help="wijk nummer)")
    parser.add_argument("n",
                        help="number of iterations", type=int)
    

    # Read arguments from command line
    args = parser.parse_args()

    # Run our line function with provided arguments
    main(args.wijk, args.n)
