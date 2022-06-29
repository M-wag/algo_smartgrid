import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from matplotlib.ticker import (MultipleLocator)
import os 
import csv

class Exporter: 
    """Class which handles function necessary to export data for Smart Grid Algorithm"""

    def __init__(self, output_info: dict) -> None:
        self.cwd = output_info['cwd']
        self.algorithm = output_info['algorithm']
        self.wijk_num = output_info['wijk_num']
        self.iterations = output_info['iterations']
        self.reset_thresh_hc = output_info['reset_thresh_hc']
        self.temperature = output_info['temperature']
        self.file_name = output_info['file_name']
        self.path_method = output_info['path_method']
        self.temp_change = output_info['temp_change']
        self.run = 0

        self.output_directory, self.output_base_name = self.get_destination_components(self.algorithm, self.wijk_num, self.path_method, self.file_name)

    def visualize_bar(self, cost_record: List[int]) -> None:

        title = f'Random algorithm neigborhood {self.wijk_num} - {self.path_method} - run{self.run}' + \
        f'\n iterations: {self.iterations}'

        fig, ax = plt.subplots()
        plt.title(title)
        plt.hist(x=cost_record, bins=100, density=True)
        plt.ylabel('Change')
        plt.xlabel('Cost')

        plt.savefig(self.get_destination() + '_bar')

    def visualize_hill(self, cost_record: List[int]) -> None:
        x_list = [x for x in range(0, len(cost_record))]

        fig, ax = plt.subplots()
        if self.algorithm == 'simulated_annealing':
            title = f'Simulated annealing neighborhood {self.wijk_num} - {self.path_method} - run{self.run}' + \
            f'\n iterations: {self.iterations}, start_temp: {self.temperature}' 
        elif self.algorithm == 'hillclimber':
            title = f'Hillclimbing neighborhood {self.wijk_num} - {self.path_method} - run{self.run}' + \
            f'\n iterations: {self.iterations}, reset_threshold: {self.reset_thresh_hc}'
        plt.title(title)
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.plot(x_list, cost_record, "-b")

        plt.savefig(self.get_destination() + '_hill')
    
    def visualize_temp(self, cost_record, temp_log):
        fig, ax = plt.subplots()
        title = f'Simulated annealing - Temperature function neighborhood {self.wijk_num}' + \
        f'\n {self.path_method}, iterations: {self.iterations}, start_temp: {self.temperature}, temp_change: {self.temp_change}' 
        plt.title(title)
        plt.xlabel('Temperature')
        plt.ylabel('Cost')
        plt.plot(temp_log, cost_record, 'bo')
        temp_directory = self.trim_path(self.get_destination(), 1)
        plt.savefig('temp_log')

    def make_csv(self, csv_data: dict)  -> None:
        """Produce a CSV or the run"""
        with open(self.get_destination() + '.csv', 'w') as file:
            writer = csv.writer(file)
            header = list(csv_data.keys())
            writer.writerow(header)
            cols = csv_data.values()

            # Check if values are unequal
            for col in list(cols):
                # Set max length
                if len(col) > 1:
                    max_len = len(col)
                # Only one length allowed for values
                if len(col) != max_len:
                    print('Values passed to CSV are of unequal length, unable to align data')

            # Unpack and Zip columns
            cols = zip(*cols)
            for row in cols: 
                writer.writerow(row)

    def draw_grid(self,
                    houses: List[Tuple[int, int]],
                    batteries: List[Tuple[int, int]],
                    paths: Tuple[int, List[List[Tuple[int, int]]]],
                    grid_cost: int):
        title = f'Grid for {self.algorithm} neighborhood {self.wijk_num} - {self.path_method} - run{self.run}' + \
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


    def get_destination_components(self, algorithm: str, wijk_number: str, path_method: str, file_name: str) -> str:
        """Returns both the directory path and the output file path """
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

    def trim_path(self, path: str, iter: int) -> str:
        """Trim the last portion of the path"""
        for i in range(iter):
            path = path.split('/')
            path.pop()
            del(path[0])
            path = ''.join(['/' + item for item in path]) 
        return path