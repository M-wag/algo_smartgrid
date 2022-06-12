import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

def visualize_grid(house_coords, battery_coords, wire_paths):
    print(wire_paths)
    fig, ax = plt.subplots()
    for path in wire_paths:
        x = []
        y = []
        for coord in path:
            x.append(coord[0])
            y.append(coord[1])
        x = np.array(x)
        y = np.array(y)
    
        plt.plot(x, y, color = 'black')

    for coord in house_coords:
        plt.scatter(coord[0], coord[1], s = 25, color='blue', marker='s')

    for coord in battery_coords:
        plt.scatter(coord[0], coord[1], s = 45, color='red', marker='s')

    # Change locators ticks to show every 20.
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    # # Set ticks to every 10
    # ax.set_xticks(np.arange(0, 50, 10))
    # ax.set_yticks(np.arange(0, 50, 10))

    plt.grid(True, which='major')
    plt.show()
    # # plt.savefig('smartgrid.jpg')
