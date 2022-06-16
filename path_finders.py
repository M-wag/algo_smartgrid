from typing import Tuple, List, Set
import random


def random_path_finder(starting_coord: Tuple[int, int],
                       end_coord: Tuple[int, int],
                       wire_segments: Set[Tuple]) -> List[Tuple[int, int]]:
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

    # Get difference between X and Y
    x_dif = x_end - x_path
    y_dif = y_end - y_path

    # pos dif = 1, neg dif = -1, no dif = 0:
    if x_dif == 0:
        next_move_x = 0
    else:
        next_move_x = int(x_dif / abs(x_dif))

    if y_dif == 0:
        next_move_y = 0
    else:
        next_move_y = int(y_dif / abs(y_dif))

    moves = []
    for x in range(abs(x_dif)):
        moves.append(("x_path", next_move_x))
    for y in range(abs(y_dif)):
        moves.append(("y_path", next_move_y))
    
    random.shuffle(moves)

    path = [(x_path, y_path)]
    
    # Draw the X line
    for move in moves:
        if move[0] == "x_path":
            x_path += move[1]
        else:
            y_path += move[1]
        path.append((x_path, y_path))

    return path
