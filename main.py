import argparse
import json
from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_cost
from visualize import visualize_grid


def main(houses_input: str, batteries_input: str, output_pictures: str, output_file: str, n: int) -> None:
    lowest_cost = 0 
    # Generate wires
    for i in range(n):
        # init
        houses = Houses(houses_input)
        batteries = Batteries(batteries_input)
        wires = Wires()
        # Make wires 
        if wires.generate(houses, batteries):
            cost = calculate_cost(houses, batteries)
            if cost < lowest_cost:
                lowest_cost = cost
                # Plot grid and save
                visualize_grid(houses.get_member_coords(),
                   batteries.get_member_coords(),
                   wires.get_paths())



if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=(
                "Generates a SmartGrid for input houses and batteries"))

    # Adding arguments
    parser.add_argument("houses_input",
                        help="input file for the houses (csv)")
    parser.add_argument("batteries_input",
                        help="input file for the batteries (csv)")
    parser.add_argument("--output_picture",
                        help="output file for the plotted grid (png)",
                        required=False)
    parser.add_argument("--output_file",
                        help="output file for lowest cost (json)",
                        required=False)
    parser.add_argument("--n",
                        help="Number of iterations",
                        required=False)

    # Read arguments from command line
    args = parser.parse_args()

    # Run our line function with provided arguments
    main(args.houses_input, args.batteries_input, args.output_pictures, args.output_file, args.n)
