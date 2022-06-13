import argparse

from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_cost
from visualize import visualize_grid


def main(houses_input: str, batteries_input: str, output: str) -> float:

    # init
    houses = Houses(houses_input)
    batteries = Batteries(batteries_input)
    wires = Wires()

    # Generate wires
    wires.generate(houses, batteries)

    # Plot grid and save
    visualize_grid(houses.get_member_coords(), batteries.get_member_coords(), wires.get_paths())

    return calculate_cost(houses, batteries)


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
