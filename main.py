# alles init
# make wires runnen
# kosten berekenen en opslaan

import argparse
from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_cost


def main(houses_input, batteries_input, output):

    # init
    houses = Houses()
    batteries = Batteries()
    wires = Wires()

    # loading
    houses.load(houses_input)
    batteries.load(batteries_input)

    # generate wires
    # TODO

    # plot grid and save
    # TODO

    return calculate_cost(houses, batteries)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=
                "Generates a SmartGrid for input houses and batteries")

    # Adding arguments
    parser.add_argument("houses_input",
        help="input file for the houses (csv)", required=True)
    parser.add_argument("batteries_input",
        help="input file for the batteries (csv)", required=True)
    parser.add_argument("output",
        help="output file for the plotted grid (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run our line function with provided arguments
    main(args.houses_input, args.batteries_input, args.output)
