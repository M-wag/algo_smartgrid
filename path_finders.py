from typing import Tuple, List


def random_path_finder(starting_coord: Tuple[int, int],
                       end_coord: Tuple[int, int]) -> List[Tuple[int, int]]:

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

    path = [(x_path, y_path)]
    # Draw the X line
    while x_path != x_end:
        x_path += next_move_x
        path.append((x_path, y_path))

    # Draw the Y line
    while y_path != y_end:
        y_path += next_move_y
        path.append((x_path, y_path))

    return path
