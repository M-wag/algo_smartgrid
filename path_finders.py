import random

def random_path_finder(starting_coord, end_coord):
	
	# Get X and Y for starting coord
	x_path = starting_coord[0]
	y_path = starting_coord[1]

	# Get X and Y for end coord
	x_end = end_coord[0]
	y_end = end_coord[1]

	
	# Get difference between X and Y
	d_x = x_end - x_path
	d_y = y_end - y_path

	# pos dif = 1, neg dif = -1, no dif = 0:
	if d_x == 0:
		next_move_x = 0
	else:
		next_move_x = int(d_x / abs(d_x))
	
	if d_y == 0:
		next_move_y = 0
	else:
		next_move_y = int(d_y / abs(d_y))
	
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