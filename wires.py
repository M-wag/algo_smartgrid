class Wire:
    def __init__(self, number, list_coor):
        self._id = number
        self._list_coor = list_coor
class Wires:
    def __init__(self):
        self.wire_list = []
        self.wire_num = 0

    def make_wire(self, battery, house):
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

        wire = Wire(self.wire_num, wire_points)
        self.wire_list.append(wire)
        self.wire_num += 1
 