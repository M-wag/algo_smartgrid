import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from matplotlib.ticker import (MultipleLocator)


def visualize_grid(house_coords: List[Tuple[int, int]],
                   battery_coords: List[Tuple[int, int]],
                   wire_paths: List[List[Tuple[int, int]]]) -> None:
    '''
    plots a figure with all houses, batteries and wire-paths

            Parameters:
                    house_coords (List[Tuple[int, int]]): 
                        A list of house coordinates
                    battery_coords (List[Tuple[int, int]]): 
                        A list of battery coordinates
                    wire_paths (List[List[Tuple[int, int]]])
                        A list of all wire-paths
    '''

    fig, ax = plt.subplots()
    for path in wire_paths:
        x = []
        y = []
        for coord in path:
            x.append(coord[0])
            y.append(coord[1])
        x = np.array(x)
        y = np.array(y)

        plt.plot(x, y, color='black')

    for coord in house_coords:
        plt.scatter(coord[0], coord[1], s=25, color='blue', marker='s')

    for coord in battery_coords:
        plt.scatter(coord[0], coord[1], s=45, color='red', marker='s')

    # Change locators ticks to show every 20.
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    # # Set ticks to every 10
    # ax.set_xticks(np.arange(0, 50, 10))
    # ax.set_yticks(np.arange(0, 50, 10))

    plt.grid(True, which='major')
    plt.show()
    plt.savefig("output.png")
