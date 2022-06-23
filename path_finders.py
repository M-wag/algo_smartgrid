from typing import Tuple, List, Set
import random
import math

def calc_distance(L1, L2, P):
    x_start, y_start = L1
    x_end, y_end = L2
    x_point, y_point = P

    distance = (abs((x_end - x_start) * (y_start - y_point) - (x_start - x_point) * (y_end - y_start)) 
                / math.sqrt(((x_end - x_start) ** 2) + ((y_end - y_start) ** 2)))
    
    return distance

def pathfinder_directions(x_path, y_path, x_end, y_end):
    # Get difference between X and Y
    x_dif = x_end - x_path
    y_dif = y_end - y_path

    # pos dif = 1, neg dif = -1, no dif = 0:
    if x_dif == 0:
        x_dir = 0
    else:
        x_dir = int(x_dif / abs(x_dif))

    if y_dif == 0:
        y_dir = 0
    else:
        y_dir = int(y_dif / abs(y_dif))

    return x_dir, y_dir

def random_pathfinder(starting_coord: Tuple[int, int],
                       end_coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    '''
    Generates a path between start- and end-coordinates,
    adds all wire segments to a set,
    returns a list of coordinates along the path.

            Parameters:
                    starting_coord (Tuple[int, int]):
                        starting point coordinates
                    end_coord (Tuple[int, int]):
                        end point coordinates
                    wire_segments (Set[Tuple[int, int, str]])
                        set with wire segment coordinates and their orientation


            Returns:
                    path (List[Tuple[int, int]]):
                        a list of all coordinates along the generated path
    '''

    # Get X and Y for starting- and end-coord
    x_path, y_path = starting_coord
    x_end, y_end = end_coord

    # get the x- and y-directions (1, -1 or 0 equal to the step size)
    x_dir, y_dir = pathfinder_directions(x_path, y_path, x_end, y_end)

    # add all the necessary moves into a list,
    # number of moves is equal to the horizontal and vertical difference
    moves = []
    for x_move in range(abs(x_end - x_path)):
        moves.append(("x_move", x_dir))

    for y_move in range(abs(y_end - y_path)):
        moves.append(("y_move", y_dir))
    
    # shuffle the order of the moves
    random.shuffle(moves)

    # add the starting point to the list and iterate over the moves
    path = [(x_path, y_path)]
    for move in moves:
        if move[0] == "x_move":
            x_path += move[1]
        else:
            y_path += move[1]
        
        # add all coordinates to the path-list
        path.append((x_path, y_path))

    return path


def hor_vert_pathfinder(starting_coord: Tuple[int, int],
                       end_coord: Tuple[int, int]) -> List[Tuple[int, int]]:

    # Get X and Y for starting- and end-coord
    x_path, y_path = starting_coord
    x_end, y_end = end_coord

    # get the x- and y-directions (1, -1 or 0 equal to the step size)
    x_dir, y_dir = pathfinder_directions(x_path, y_path, x_end, y_end)

    # add the starting coordinate to the path-list
    path = [(x_path, y_path)]

    # Draw the horizontal line
    while x_path != x_end:
        x_path += x_dir
        path.append((x_path, y_path))
    
    # Draw the vertical line
    while y_path != y_end:
        y_path += y_dir
        path.append((x_path, y_path))

    return path

def straight_pathfinder(starting_coord: Tuple[int, int],
                       end_coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    # Get X and Y for starting- and end-coord
    x_path, y_path = starting_coord
    x_end, y_end = end_coord

    # get the x- and y-directions (1, -1 or 0 equal to the step size)
    x_dir, y_dir = pathfinder_directions(x_path, y_path, x_end, y_end)

    path = [(x_path, y_path)]
    
    while (x_path, y_path) != (x_end, y_end):
        x_test = (x_path + x_dir, y_path)
        y_test = (x_path, y_path + y_dir)

        # calculate distance from the two point to the house-battery line
        x_move_dis = calc_distance(starting_coord, end_coord, x_test)
        y_move_dis = calc_distance(starting_coord, end_coord, y_test)

        # choose the option closest to the line, favoring the x_direction
        if x_path == x_end:
            y_path += y_dir
        elif y_path == y_end:
            x_path += x_dir
        elif x_move_dis <= y_move_dis:
            x_path += x_dir
        else:
            y_path += y_dir
        
        # add the resulting coordinate to the path-list
        path.append((x_path, y_path))
    
    return path
