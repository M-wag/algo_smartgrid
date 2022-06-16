import argparse
import json
from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_shared_cost
from visualize import visualize_grid, visualize_bar


def main(wijk_num: str, n: int, save_changes: bool) -> None:
    lowest_cost = 1000000
    cost_record = []
    # Generate wires
    for i in range(n):
        # init
        houses = Houses(f'data/district_{wijk_num}/district-{wijk_num}_houses.csv')             # noqa: E501
        batteries = Batteries(f'data/district_{wijk_num}/district-{wijk_num}_batteries.csv')    # noqa: E501
        wires = Wires()

        # Make wires
        if wires.generate(houses, batteries):
            wires.share_wires()
            cost = calculate_shared_cost(wires, batteries)
            cost_record.append(cost)
            print(f"iteration: {i}  cost: {cost}")
            if cost < lowest_cost:
                lowest_cost = cost
                # Plot grid and save
                if save_changes is True:
                    visualize_grid(houses.get_member_coords(),
                    batteries.get_member_coords(),
                    wires.get_paths(), f'output/smartgrid_wijk_{wijk_num}.png')
        else:
            print(i,'No valid outcome')

    if save_changes is True:
        dict_json = { "district" : wijk_num, "own-costs" : lowest_cost}
        json_object = json.dumps(dict_json, indent = 2)
        with open(f'output/smartgrid_wijk_{wijk_num}.json', "w") as outfile:
            outfile.write(json_object)
    
    visualize_bar(cost_record)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=(
                "Generates a SmartGrid for input houses and batteries"))

    # Adding arguments
    parser.add_argument("wijk",
                        help="wijk number)")
    parser.add_argument("n",
                        help="number of iterations", type=int)
    parser.add_argument("save_changes",
                        help="whether to save output to files", type=bool)
    

    # Read arguments from command line
    args = parser.parse_args()

    # Run our line function with provided arguments
    main(args.wijk, args.n, args.save_changes)
