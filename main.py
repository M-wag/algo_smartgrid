import argparse
import json
from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_shared_cost, calculate_own_cost
from visualize import visualize_grid, visualize_bar

def hillclimber(houses, wires, batteries):
    house_1 = houses.random_pick()
    house_2 = houses.random_pick()
    while new_wires == False:
        new_wires = wires.swap(house_1, house_2)
    new_cost = calculate_shared_cost(new_wires, batteries)
    return new_cost, new_wires

def main(wijk_num: str, iterations: int, save_changes: bool, n) -> None:
    cost_record = []
    count = 0
    # init
    houses = Houses(f'data/district_{wijk_num}/district-{wijk_num}_houses.csv')             # noqa: E501
    batteries = Batteries(f'data/district_{wijk_num}/district-{wijk_num}_batteries.csv')    # noqa: E501
    wires = Wires()
    grid = False
    while grid == False:
        grid = wires.generate(houses, batteries)
    wires.share_wires()
    cost = calculate_shared_cost(wires, batteries)
    cost_record.append(cost)
    for i in range(iterations):
        new_cost, new_wires = hillclimber(houses, wires, batteries)
        if new_cost <= cost:
            cost = new_cost
            wires.wires = new_wires
            count = 0
        else:
            count += 1
        if count == n:
            grid = False
            while grid == False:
                grid = wires.generate(houses, batteries)
                # Plot grid and save
    if save_changes is True:
        visualize_grid(houses.get_member_coords(),
        batteries.get_member_coords(),
        wires.get_paths(), f'output/smartgrid_wijk_{wijk_num}.png')

        dict_json = { "district" : wijk_num, "shared-costs" : cost}
        json_object = json.dumps(dict_json, indent = 2)
        with open(f'output/smartgrid_wijk_{wijk_num}.json', "w") as outfile:
            outfile.write(json_object)
            
        visualize_bar(cost_record, f'output/wijk_{wijk_num}_bar.png')
    


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
