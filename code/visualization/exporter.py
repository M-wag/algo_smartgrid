import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from matplotlib.ticker import (MultipleLocator)
import os 

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
        self.run = 0

        self.output_directory, self.output_base_name = self.get_destination_components(self.algorithm, self.wijk_num, self.path_method, self.file_name)
    
    def draw_plot(self, cost_record: List[int], graph: str) -> None:
        """Save a plot of the produce algorithm data"""

        fig, ax = plt.subplots()
        plt.ylabel('Iterations')
        plt.xlabel('Cost')
        plt.ylim(bottom = 0)
        plt.title(self.get_title('plot', 0))

        if graph == 'bar':
            rounded_cost_record = [round(i, 2) for i in cost_record]
            values, counts = np.unique(rounded_cost_record, return_counts=True)
            plt.bar(x=values, height=counts, width=90)
            tag = '_bar'
        elif graph == 'line':
            x_list = [x for x in range(0, len(cost_record))]
            plt.plot(x_list, cost_record, "-b")
            tag = '_hill'

        plt.savefig(self.get_destination() + tag)

    def draw_grid(self,
                    houses: List[Tuple[int, int]],
                    batteries: List[Tuple[int, int]],
                    paths: Tuple[int, List[List[Tuple[int, int]]]],
                    grid_cost: int):

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
            plt.title(self.get_title('grid', grid_cost))
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
    
    def get_title(self, vis_target: str, cost: int) -> str:
        """Produce a title for a generate figure"""
        if  vis_target == 'plot':
            if self.algorithm == 'simulated_annealing':
                title = f'Simulated annealing of wijk{self.wijk_num} using {self.path_method} path method (run{self.run})' + \
                f'\n iterations: {self.iterations}, temp_start: {self.temperature}' 
            elif self.algorithm == 'hillclimber':
                title = f'Hillclimbing of wijk{self.wijk_num} using {self.path_method} path method (run{self.run})' + \
                f'\n iterations: {self.iterations}, reset_threshold: {self.reset_thresh_hc}' 
            elif self.algorithm == 'random':
                title = f'Random Baseline algorithm of wijk{self.wijk_num} using {self.path_method} path method (run{self.run})' + \
                f'\n iterations: {self.iterations} '
            else:
                title = f'Cost for {self.algorithm} of wijk {self.wijk_num} using {self.path_method} (run{self.run})' + \
                f'\n iterations: {self.iterations}, cost: {cost}'
        elif vis_target =='grid':
            if self.algorithm == 'annealing':
                title = f'Grid for simulated annealing of wijk{self.wijk_num} using {self.path_method} path method (run{self.run})' + \
                f'\n iterations: {self.iterations}, temp_start: {self.temperature}, cost: {cost}' 
            elif self.algorithm == 'hillclimber':
                title = f'Grid for hillclimbing of wijk{self.wijk_num} using {self.path_method} path method (run{self.run})' + \
                f'\n iterations: {self.iterations}, reset_threshold: {self.reset_thresh_hc}, cost: {cost}' 
            elif self.algorithm == 'random':
                title = f'Grid for random baseline algorithm of wijk{self.wijk_num} using {self.path_method} path method (run{self.run})' + \
                f'\n iterations: {self.iterations}, cost: {cost} '
            else:
                title = f'Grid for {self.algorithm} of wijk {self.wijk_num} using {self.path_method} (run{self.run})' + \
                f'\n iterations: {self.iterations}, cost: {cost}'
        
        return title

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