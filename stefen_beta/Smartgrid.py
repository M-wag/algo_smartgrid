import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


class Cell():

    def __init__ (self):
        self._container = {"house_id": None, "battery_id": None, "wire_id": []}
    
    def add_item(self, type, id):
        if type == "wire_id":
            self._container[type].append(id)
        else:
            self._container[type] = id
    
    def get_id(self):
        return self._container["house_id"]
    
    # 0 : empty
    # 1 : house
    # 2 : battery
    # 3 : wirepoint
    def value(self):
        if self._container["house_id"] != None:
            return 1
        elif self._container["battery_id"] != None:
            return 2
        elif len(self._container["wire_id"]) != 0:
            return 3
        else:
            return 0    


class SmartGrid():

    def __init__(self, houses_csv, batteries_csv):
        
        self._wire_points = 0

        # initialise grid of type object
        self._grid = np.ndarray((51, 51),dtype=object)

        # read the houses-file and store the information consisting of tuples
        # example: (x, y, output)
        # with its index being its id
        houses_df = pd.read_csv(f"Huizen&Batterijen/district_1/{houses_csv}")
        self._houses_info = houses_df.apply(tuple, axis=1).tolist()

        # read the batteries-file and this time storing them as lists instead
        # this way we can change the capacity-value
        # example: [x, y, capacity]
        batteries_df = pd.read_csv(f"Huizen&Batterijen/district_1/{batteries_csv}")
        split_coords = batteries_df["positie"].str.split(',', expand=True)
        batteries_df = pd.concat([split_coords, batteries_df], axis=1).drop("positie", axis=1)
        batteries_df[[0, 1]] = batteries_df[[0, 1]].apply(pd.to_numeric)
        self._batteries_info = batteries_df.apply(list, axis=1).tolist()

        # fill the grid with unique Cell-objects
        for row_nr in range(51):
            for column_nr in range(51):
                self._grid[row_nr, column_nr] = Cell()

        # add houses to their corresponding coordinates on the grid
        for id, house in enumerate(self._houses_info):
            self._grid[int(house[0]), int(house[1])].add_item("house_id", id)
        
        # add batteries to their corresponding coordinates on the grid
        for id, battery in enumerate(self._batteries_info):
            self._grid[int(battery[0]), int(battery[1])].add_item("battery_id", id)

    """help function for sorting"""
    def sort_distance(self, elem):
        return elem[1]

    """function for creating the house-battery pairs""" 
    def wire_layout(self):
        for house in self._houses_info:
            distances = []

            # for every battery, calculate distance to house and append to list with id
            for id, battery in enumerate(self._batteries_info):
                distance = abs(house[0] - battery[0]) + abs(house[1] - battery[1])
                distances.append(tuple([id, distance]))
            
            # sort the id, distance pairs according to their distance
            distances.sort(key=self.sort_distance)

            # begin with the battery with the shortest distance
            for battery in distances:

                # check if the battery-capacity has not been reached yet
                if self._batteries_info[battery[0]][2] - house[2] >= 0:

                    # subtract the output from the capacity and call wiremaker
                    self._batteries_info[battery[0]][2] -= house[2]
                    self.make_wire(battery, house)
                    break

    """create wire between battery and house"""
    def make_wire(self, battery, house):
        wire_points = []
        battery_x, battery_y = self._batteries_info[battery[0]][:2]
        house_x, house_y = house[:2]

        # calculate x and y difference
        x_dif = house_x - battery_x
        y_dif = house_y - battery_y

        # calculate x and y direction, normalised to 1 and -1
        # failsafe zodat we zometeen geen divide by zero error hebben
        # heel sloppy i know
        if x_dif == 0:
            x_direction = 0
        else:
            x_direction = x_dif / abs(x_dif)
        if y_dif == 0:
            y_direction = 0
        else:
            y_direction = y_dif / abs(y_dif)

        # draw the longer axis first
        if abs(x_dif) > abs(y_dif):

            # append wire coordinates to list
            wire_points.append(tuple([battery_x, battery_y]))
            while house_x != battery_x:
                battery_x += x_direction
                wire_points.append(tuple([battery_x, battery_y]))
            while house_y != battery_y:
                battery_y += y_direction
                wire_points.append(tuple([battery_x, battery_y]))
        else:
            while house_y != battery_y:
                battery_y += y_direction
                wire_points.append(tuple([battery_x, battery_y]))
            while house_x != battery_x:
                battery_x += x_direction
                wire_points.append(tuple([battery_x, battery_y]))
        
        # add every wire point to their respective cell, 
        # id being the destination house
        for point in wire_points:
            self._wire_points += 1
            self._grid[int(point[0]), int(point[1])].add_item("wire_id", 
            self._grid[int(house_x), int(house_y)].get_id())
        
    """returns a representation of the grid with values in between 0-3""" 
    def status(self):
        new_grid = []
        for row_nr in range(51):
            row = []
            for column_nr in range(51):
                row.append(self._grid[column_nr, row_nr].value())
            new_grid.append(row)
        return new_grid

    """returns the total amount of wire used""" 
    def calculate_wires(self):
        return self._wire_points - len(self._houses_info)


smartgrid = SmartGrid("district-1_houses.csv", "district-1_batteries.csv")
smartgrid.wire_layout()
print(smartgrid.calculate_wires())

# save the grid as a heatmap
fig = plt.figure()
cmap = ListedColormap(["white", "red", "black", "blue"])

plt.imshow(smartgrid.status(), origin='lower', cmap=cmap)

plt.savefig("output.png")


