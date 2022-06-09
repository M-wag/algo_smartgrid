import pandas as pd
from house import House
from battery import Battery
from wire import Wire
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

def main():
    # Load Battery Battery
    battery_data = pd.read_csv('battery_data.csv')
    # Initialize Battery
    all_batteries = {}
    for index,row in battery_data.iterrows():
        battery_id = row.name
        pos = row['positie'].split(',')
        pos = tuple(int(number) for number in pos)
        capacity = row['capaciteit']
        all_batteries[battery_id] = Battery(battery_id, pos, capacity)
    # print([battery.position for battery in all_batteries.values()])

    # Load House Position
    house_data = pd.read_csv('house_data.csv')
    # Initalize Houses
    all_houses = {}
    batteries_pos = {battery.id : battery.position for battery in all_batteries.values()}
    for index,row in house_data.iterrows():
        house_id = row.name
        pos = (row['x'], row['y'])
        max_output = row['maxoutput']
        #   Get the ID of all batteries, sorted by how close they are to hosue
        dist_order_bats = order_by_distance(pos, batteries_pos)
        all_houses[house_id] = House(house_id, pos, max_output, dist_order_bats)

    all_wires = {}
    for house in all_houses.values():
        for battery_id in house.closest_bats:
            battery = all_batteries[battery_id]
            if battery.can_connect(house.max_output):
                connect(house, battery)
                # Connect wires
                wire_id = house.id
                house_coord = house.position
                battery_coord = house.battery.position
                wire_path = get_path(house_coord, battery_coord)
                # Save wire
                wire = Wire(wire_id, house, house.battery, wire_path)
                all_wires[wire_id] = wire
                house.add_wire(wire)
                battery.add_wire(wire)
                break
    visualize_grid(all_houses, all_batteries, all_wires)

def order_by_distance(coord: set, target_coords: dict) -> list:
    """Reutn which coordinates are closest in list"""

    ordered_distances = {}
    for i in range(len(target_coords)): 
        target_coord = target_coords[i]
        target_id = list(target_coords.keys())[i]
        dist = math.dist(coord, target_coord)
        ordered_distances[target_id] = dist
    ordered_distances = dict(sorted(ordered_distances.items(), key=lambda x: x[1]))
    closest_targets = list(ordered_distances.keys()) 

    return closest_targets

def get_path(coord1: set, coord2: set) -> list:
    return [coord1, coord2]
    
def connect(house, battery):
    house.connect(battery)
    battery.connect(house)

def visualize_grid(houses, batteries, wires):
    fig, ax = plt.subplots()
    for wire in wires.values():
        x = []
        y = []
        for coord in wire.wire_path:
            x.append(coord[0])
            y.append(coord[1])
        x = np.array(x)
        y = np.array(y)
    
        plt.plot(x, y, color = 'black')

    for house in houses.values():
        coord = house.position
        plt.scatter(coord[0], coord[1], s = 25, color='blue', marker='s')


    # Change major ticks to show every 20.
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    plt.grid(True, which='major')
    plt.show()
    # plt.savefig('smartgrid.jpg')

main()