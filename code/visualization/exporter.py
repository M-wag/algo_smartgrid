import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from matplotlib.ticker import (MultipleLocator)
import os 
import json

class Exporter: 
    """Class which handles function necessary to export data for Smart Grid Algorithm"""

    def __init__(self, output_info: dict) -> None:
        self.cwd = output_info['cwd']
        self.algorithm = output_info['algorithm']
        self.district_num = output_info['district_num']
        self.iterations = output_info['iterations']
        self.reset_thresh_hc = output_info['reset_thresh_hc']
        self.temperature = output_info['temperature']
        self.file_name = output_info['file_name']
        self.path_method = output_info['path_method']
        self.start_state = output_info['start_state']
        self.temp_change = output_info['temp_change']
        self.run = 0

        self.output_directory, self.output_base_name = self.get_destination_components(self.algorithm, self.district_num, self.path_method, self.file_name)

    def visualize_bar(self, cost_record: List[int]) -> None:
        '''Makes a bar plot'''
        title = f'Random algorithm neigborhood {self.district_num} - {self.path_method} - run{self.run}' + \
        f'\n iterations: {self.iterations}'

        fig, ax = plt.subplots()
        plt.title(title)
        plt.hist(x=cost_record, bins=100, density=True)
        plt.ylabel('Chance')
        plt.xlabel('Cost')

        plt.savefig(self.get_destination() + '_bar')

    def visualize_hill(self, cost_record: List[int]) -> None:
        '''Make a line plot'''
        x_list = [x for x in range(0, len(cost_record))]

        fig, ax = plt.subplots()
        if self.algorithm == 'simulated_annealing':
            title = f'Simulated annealing neighborhood {self.district_num} - {self.path_method} - run{self.run}' + \
            f'\n iterations: {self.iterations}, start_temp: {self.temperature}' 
        elif self.algorithm == 'hillclimber':
            title = f'Hillclimbing neighborhood {self.district_num} - {self.path_method} - run{self.run}' + \
            f'\n iterations: {self.iterations}, reset_threshold: {self.reset_thresh_hc}'
        plt.title(title)
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.plot(x_list, cost_record, "-b")

        plt.savefig(self.get_destination() + '_hill')
    
    def visualize_hill_kmean(self, cost_record, score_record):
        '''Make al line plot for the kmeans algoritme'''
        x_list_cost = [x for x in range(0, len(cost_record))]
        x_list_score = [x for x in range(0, len(score_record))]

        if len(score_record) == 0:
            fig, ax = plt.subplots()
            title = f'Simulated annealing neighborhood {self.district_num} - {self.path_method} - run{self.run}' + \
            f'\n iterations: {self.iterations}, start_temp: {self.temperature}, start_state: random' 
            plt.title(title)
            plt.xlabel('Iterations')
            plt.ylabel('Cost')
            plt.plot(x_list_cost, cost_record, "-b")
        else:
            fig, (ax1, ax2) = plt.subplots(1, 2)
            title = f'Simulated annealing neighborhood {self.district_num} - {self.path_method} - run{self.run}' + \
            f'\n iterations: {self.iterations}, start_temp: {self.temperature}, start_state: simulated annealing' 
            fig.suptitle(title)
            ax1.set_xlabel('Iterations')
            ax1.set_ylabel('Score')
            ax1.plot(x_list_score, score_record, "-b")
            ax2.set_xlabel('Iterations')
            ax2.set_ylabel('Cost')
            ax2.plot(x_list_cost, cost_record, "-b")

        plt.savefig(self.get_destination() + '_hill')
    
    def visualize_temp(self, cost_record, temp_log):
        '''Make a dot plot for all the differnt costs and temperatures for simulated annealing'''
        fig, ax = plt.subplots()
        title = f'Simulated annealing - Temperature function neighborhood {self.district_num}' + \
        f'\n {self.path_method}, iterations: {self.iterations}, start_temp: {self.temperature}, temp_change: {self.temp_change}' 
        plt.title(title)
        plt.xlabel('Temperature')
        plt.ylabel('Cost')
        plt.plot(temp_log, cost_record, 'bo')

        plt.savefig(self.get_destination() + '_temp_log')
        

    def draw_grid(self,
                    houses: List[Tuple[int, int]],
                    batteries: List[Tuple[int, int]],
                    paths: Tuple[int, List[List[Tuple[int, int]]]],
                    grid_cost: int):
        '''Makes a grid visualizing all the wires, batteries and houses'''
        title = f'Grid for {self.algorithm} neighborhood {self.district_num} - {self.path_method} - run{self.run}' + \
                f'\n iterations: {self.iterations}, cost: {grid_cost}'
        fig, ax = plt.subplots()
        colors = ["red", "blue", "green", "purple", "black"]

        for bat_id, path in paths:
            x = []
            y = []
            for coord in path:
                x.append(coord[0])
                y.append(coord[1])
            x = np.array(x)
            y = np.array(y)

            plt.plot(x, y , color=colors[bat_id])
            plt.title(title)
            ax.set_yticklabels([])
            ax.set_xticklabels([])

        for house in houses:
            plt.scatter(house.position[0], house.position[1], s=25, color=colors[house.battery.id], marker='s')

        for battery in batteries:
            plt.scatter(battery.position[0], battery.position[1], s=45, color=colors[battery.id], marker='s')

        # Change locators ticks to show every 20.
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))

        plt.grid(True, which='major')
        plt.savefig(self.get_destination() + '_grid')


    def get_destination(self) -> str:
        """Return the file destination, make directory if doesn;t alread exist"""
        destination = self.cwd + '/output/' + self.output_directory + f'run{self.run}/' + self.output_base_name + f'_run{self.run}'
        destination_parent = self.cwd + '/output/' + self.output_directory + f'run{self.run}/' 
        # Produce directory if it does not exist
        if os.path.exists(destination_parent) == False:
            os.makedirs(destination_parent)
        return destination


    def get_destination_components(self, algorithm: str, district_number: str, path_method: str, file_name: str) -> str:
        """Returns both the directory path and the output file path """
        directory_path = f'{algorithm}/wijk{district_number}/{path_method}/{file_name}/'
        
        param_acronyms = {
            'hillclimber' : 'hc',
            'random' : 'rand',
            'simulated_annealing' : 'sa',
            'kmean' : 'km',
            'hor_ver' : 'hv',
            'straight' : 'str'
        }
        output_name = f'{file_name}_{param_acronyms[algorithm]}_w{district_number}_{param_acronyms[path_method]}'

        return directory_path, output_name

    def make_json(self, lowest_cost, district_num, lowest_batteries):
        '''Makes a json file of alle the wires, houses and batteries with the district number and the cost'''
        dict_json = [{"district": district_num, "costs-shared": lowest_cost}]
        for battery in lowest_batteries.get_members():
            battery_dict = {"location": f'{battery.position[0]},{battery.position[1]}' ,"capacity": battery.capacity, "houses" :[]}
            for house in battery.houses.values():
                house_dict = {"location": f'{house.position[0]},{house.position[1]}', "output": house.max_output}
                cables = []
                for wire_point in house.wire.path:
                    str_wire = f'{wire_point[0]},{wire_point[1]}'
                    cables.append(str_wire)
                    house_dict['cables'] = cables
                battery_dict['houses'].append(house_dict)
            dict_json.append(battery_dict)
        json_object = json.dumps(dict_json, indent = 2)
        with open(self.get_destination() + '_grid.json', "w") as outfile:
            outfile.write(json_object)