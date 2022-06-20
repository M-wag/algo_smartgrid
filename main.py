import argparse
from copy import deepcopy
import json
from houses import Houses
from batteries import Batteries
from wires import Wires
from calculator import calculate_shared_cost, calculate_own_cost
from visualize import visualize_grid, visualize_bar, visualize_hill

def hillclimber(houses, wires):
    new_wires = False
    while new_wires == False:
        house_list = houses.random_pick()
        new_wires = wires.swap(house_list[0], house_list[1])
    return new_wires

def main(wijk_num: str, iterations: int,  restart, save_changes: bool,) -> None:
    cost_record = []
    count = 0
    # init
    og_houses = Houses(f'data/district_{wijk_num}/district-{wijk_num}_houses.csv')             # noqa: E501
    og_batteries = Batteries(f'data/district_{wijk_num}/district-{wijk_num}_batteries.csv')    # noqa: E501
    og_wires = Wires()
    lowest_cost = 999999
    for i in range(iterations):
        houses = deepcopy(og_houses)
        batteries = deepcopy(og_batteries)
        wires = deepcopy(og_wires)
        grid = False
        while grid == False:
            grid = wires.generate(houses, batteries)
        wires.shared_wires = wires.share_wires(wires.wires)
        cost = calculate_shared_cost(wires.shared_wires, batteries)
        cost_record.append(cost)
        count = 0
        while count < restart:
<<<<<<< HEAD
=======

            print(f"iteration {i}, cost {cost}")
>>>>>>> 8c910f82237620a9ad0e8776a340cc2df9a40bae
            new_wires = hillclimber(houses, wires)
            new_shared_wires = wires.share_wires(new_wires)
            new_cost = calculate_shared_cost(new_shared_wires, batteries)
            if new_cost <= cost:
                cost = new_cost
                wires.wires = new_wires
                wires.shared_wires = new_shared_wires
                count = 0
            else:
                count += 1
            cost_record.append(cost)
        if cost < lowest_cost:
            lowest_cost = cost
    print(lowest_cost)
    # Plot grid and save
    if save_changes is True:
        visualize_grid(houses.get_member_coords(),
        batteries.get_member_coords(),
        wires.get_paths(), f'output/smartgrid_wijk_{wijk_num}.png')

        dict_json = {"district" : wijk_num, "shared-costs" : cost}
        json_object = json.dumps(dict_json, indent = 2)
        with open(f'output/smartgrid_wijk_{wijk_num}.json', "w") as outfile:
            outfile.write(json_object)

        visualize_hill(cost_record, f'output/wijk_{wijk_num}_hill.png')
    


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=(
                "Generates a SmartGrid for input houses and batteries"))

    # Adding arguments
    parser.add_argument("wijk",
                        help="wijk number)")
    parser.add_argument("iterations",
                        help="number of iterations", type=int)
    parser.add_argument("restart",
                        help="number of iterations", type=int)
    parser.add_argument("save_changes",
                        help="whether to save output to files", type=bool)
    

    # Read arguments from command line
    args = parser.parse_args()

    # Run our line function with provided arguments
    main(args.wijk, args.iterations, args.restart, args.save_changes,)
