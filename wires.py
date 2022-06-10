# class wire & class wires met make functie
class Wires:
    def __init__(self):
        

    def make_wire(battery, house, wire_num):
        wire_points = []
        battery_x, battery_y = battery
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
            wire_points.append((wire_x, wire_y))

        while house_y != (wire_y + y_direction):
            wire_y += y_direction
            wire_points.append((wire_x, wire_y))

        wire = Wire(wire_num, wire_points)
        return wire


class Wire:
    def __init__(self, number, list_coor):
        self._id = number
        self._list_coor = list_coor

    