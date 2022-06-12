# alles init
# make wires runnen
# kosten berekenen en opslaan

import argparse
from urllib.robotparser import RequestRate

from regex import W
from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_cost
# import visualize_grid


def main(houses_input, batteries_input, output):

    # init
    houses = Houses()
    batteries = Batteries()
    wires = Wires()

    # loading
    houses.load(houses_input)
    batteries.load(batteries_input)

        # Test: Loading works
        # print(houses.dict_houses)
        # print(batteries.dict_batteries)

    # Generate wires
    wires.generate(houses, batteries)

    # Plot grid and save
    # visualize_grid(houses.get_coords, batteries.get_coords, wires.get_paths)

    return calculate_cost(wires, batteries)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=
                "Generates a SmartGrid for input houses and batteries")

    # Adding arguments
    parser.add_argument("houses_input",
        help="input file for the houses (csv)")
    parser.add_argument("batteries_input",
        help="input file for the batteries (csv)")
    parser.add_argument("--output",
        help="output file for the plotted grid (png)", required=False)

    # Read arguments from command line
    args = parser.parse_args()

    # Run our line function with provided arguments
    main(args.houses_input, args.batteries_input, args.output)
