class Battery():
    def __init__(self,id,  position, capacity):
        self.id = id
        self.position = position
        self.capacity = capacity
        self.houses = []
        self.total_input = 0
        self.wires = []
    
    def can_connect(self, house_output):
        if self.total_input + house_output > self.capacity:
            return False
        else:
            return True

    def connect(self, house):
        self.houses.append(house)
        self.total_input += house.max_output
    
    def add_wire(self, wire):
        self.wires.append(wire)
        
        