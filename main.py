import argparse
from code.classes.houses import Houses
from code.classes.batteries import Batteries
from code.classes.wires import Wires
from code.algorithms.hillclimber import hillclimber
from code.algorithms.simulated_annealing import simulated_annealing
from code.algorithms.random_algo import random_algo
from code.algorithms.kmean_simulated_annealing import kmean_simulated_annealing
from code.visualization.exporter import Exporter
import os

max_restart_boundary = 2500
max_iterations = 1000000
max_temperature = 10000
max_temperature_change = 500
max_reruns = 100

def main(algorithm, wijk_num: str, iterations: int, restart_hillclimber, temperature, temp_change, file_name, reruns, type_wires, start_state) -> None:
    # Get current working directory of ran file. Generate directory with classes and directory for outputs
    cwd = os.path.dirname(os.path.abspath(__file__))
    class_directory = cwd + f'/data/district_{wijk_num}/district-{wijk_num}_'

    output_params = {
        'cwd' : cwd,
        'algorithm' : algorithm,
        'wijk_num' : wijk_num,
        'iterations' : iterations,
        'reset_thresh_hc' : restart_hillclimber,
        'temperature' : temperature,
        'file_name' : file_name,
        'path_method' : type_wires,
        'start_state' : start_state,
        'temp_change' : temp_change
    }

    exporter = Exporter(output_params)
    temp_log = []
    lowest_cost_record = []
    for rerun in range(reruns):
        houses = Houses(class_directory + 'houses.csv')
        batteries = Batteries(class_directory + 'batteries.csv')
        wires = Wires(type_wires)

        if algorithm == 'hillclimber':
            lowest_cost, lowest_wires, lowest_batteries, cost_record = hillclimber(iterations, restart_hillclimber, wires, batteries, houses)
            exporter.visualize_hill(cost_record)
        elif algorithm == 'random':
            lowest_cost, lowest_wires, lowest_batteries, cost_record = random_algo(iterations, wires, batteries, houses)
            exporter.visualize_bar(cost_record)
        elif algorithm == 'simulated_annealing':
            lowest_cost, lowest_wires, lowest_batteries, cost_record = simulated_annealing(iterations, temperature, wires, batteries, houses)
            temperature = temperature - temp_change
            temp_log.append(temperature)
            lowest_cost_record.append(lowest_cost)
            exporter.visualize_hill(cost_record)
        elif algorithm == 'kmean':
            lowest_cost, lowest_wires, lowest_batteries, cost_record, score_record = kmean_simulated_annealing(iterations, temperature, wires, batteries, houses, start_state, type_wires)
            temperature = temperature - temp_change
            temp_log.append(temperature)
            lowest_cost_record.append(lowest_cost)
            exporter.visualize_hill_kmean(cost_record, score_record)
        else:
            print('Invalid argument passed to main')
            quit()

        # Save Grid Plot
        exporter.draw_grid(houses.get_members(), batteries.get_members(), lowest_wires.get_paths(), lowest_cost)
        exporter.make_json(lowest_cost, wijk_num, lowest_batteries)
       
        # Increment run
        exporter.run += 1
    
    if algorithm == 'simulated_annealing':
        print(lowest_cost_record)
        print(temp_log)
        exporter.visualize_temp(lowest_cost_record, temp_log)
        
def get_output_path(algorithm: str, wijk_number: str, path_method: str, file_name: str) -> str:
    """
    Returns both the directory path and the output file path
    Parameters
    ----------
    """
    directory_path = f'{algorithm}/wijk{wijk_number}/{path_method}/{file_name}/'
    
    param_acronyms = {
        'hillclimber' : 'hc',
        'random' : 'rand',
        'simulated_annealing' : 'sa',
        'hor_ver' : 'hv',
        'straight' : 'str'
    }
    output_name = f'{file_name}_{param_acronyms[algorithm]}_w{wijk_number}_{param_acronyms[path_method]}'

    return directory_path, output_name

    
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
        if pos_int < 0:
            print('Make sure the integer is positive')
            continue
        if pos_int > upper_limit:
            print('Passed integer exceeds the upper limit')
            continue
        return pos_int


if __name__ == "__main__":
    # List of viable algorithms
    viable_algorithms = ['hillclimber', 'simulated_annealing',
                         'random', 'kmean']

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description=(
                "Generates a SmartGrid for input houses and batteries"))

    # Adding arguments
    parser.add_argument("algorithm",
                        help="algorithm type)")

    # Read arguments from command line
    args = parser.parse_args()
    if args.algorithm not in viable_algorithms:
        print('Invald algorithm passed to command line')
        quit()

    wijk = get_positive_int('Select neighborhoud: ', 3) 
    iterations = get_positive_int('Iteration amount: ', max_iterations)
    type_wires = input('Type of wires: straight or hor_ver: ')
    file_name = input('File name: ')
    reruns = get_positive_int('Number of runs: ', max_reruns)

    if args.algorithm == 'hillclimber':
        hill_restart = get_positive_int('Restart boundary for hill climber: ', max_restart_boundary)
        temperature = 1
        temp_change = 1
        start_state = 1
    elif args.algorithm == 'simulated_annealing': 
        temperature = get_positive_int('Temperature for simulated annealing: ', max_temperature)
        temp_change = get_positive_int('Temperature change per run for simulated annealing: ', max_temperature_change)
        hill_restart = 1
        start_state = 1
    elif args.algorithm == 'random':
        hill_restart = 1
        temperature = 1
        temp_change = 1
        start_state = 1
    elif args.algorithm == 'kmean':
        temperature = get_positive_int('Temperature for simulated annealing: ', max_temperature)
        temp_change = get_positive_int('Temperature change per run for simulated annealing: ', max_temperature_change)
        start_state = input('Start state algorithm: ')
        if start_state not in ['random', 'simulated_annealing']:
            print('Invald algorithm passed to command line')
            quit()
        hill_restart = 1
        
    # Run our line function with provided arguments
    main(args.algorithm, wijk, iterations, hill_restart, temperature, temp_change, file_name, reruns, type_wires, start_state)
