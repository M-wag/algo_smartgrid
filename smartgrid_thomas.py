import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import random

class House:
    def __init__(self, number, x, y, output):
        self._id = number
        self._output = output
        self._cabel = None
        self._coor = (x, y) 

class Battery:
    def __init__(self, number, x, y, capaciteit):
        self._id = number
        self._capaciteit = capaciteit
        self._coor = (x, y)
        self._houses = []

class Wire:
    def __init__(self, number, list_coor):
        self._id = number
        self._list_coor = list_coor

def make_wire(grid, battery, house, wire_num):
    wire_points = []
    battery_x, battery_y = battery
    print(house)
    house_x, house_y = house
    wire_x = battery_x
    wire_y = battery_y

    x_dif = house_x - battery_x
    y_dif = house_y - battery_y
    
    if x_dif == 0:
        x_direction = 0
    else:
        x_direction = int(x_dif / abs(x_dif))
    if y_dif == 0:
        y_direction = 0
    else:
        y_direction = int(y_dif / abs(y_dif))

    while house_x != (wire_x + x_direction):
        wire_x += x_direction
        print(x_direction)
        wire_points.append((wire_x, wire_y))
        print(wire_x)
        grid[wire_x][wire_y] = 3

    while house_y != (wire_y + y_direction):
        wire_y += y_direction
        wire_points.append((wire_x, wire_y))
        grid[wire_x][wire_y] = 3

    wire = Wire(wire_num, wire_points)
    return wire

if __name__ == "__main__":
    grid = np.zeros((51, 51))

    df_houses = pd.read_csv('district-1_houses.csv')
    df_batteries =  pd.read_csv('district-1_batteries.csv')

    houses = []
    for index, row in df_houses.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        house = House(index, x, y, row['maxoutput'])
        houses.append(house)
        grid[x][y] = 1

    batteries = []
    for index, row in df_batteries.iterrows():
        x, y = row['positie'].split(',')
        battery = Battery(index, int(x), int(y), row['capaciteit'])
        batteries.append(battery)
        grid[int(x)][int(y)] = 2

    i = 0
    wires = []
    houses = random.shuffle(houses)
    for house in houses:
        battery = random.choice(batteries)
        wire = make_wire(grid, battery._coor, house._coor, i)
        wires.append(wire)

    fig, ax = plt.subplots()
    colors_list = ['white', 'green', 'red', 'blue']
    cmap = colors.ListedColormap(colors_list)
    bounds = [0,1,2,3,4]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    im = ax.imshow(grid, cmap=cmap, norm=norm)
    plt.show()


