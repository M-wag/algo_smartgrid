class House():
    def __init__(self, id , position, max_output, closest_bats):
        self.id = id
        self.position = position
        self.max_output = max_output
        self.closest_bats = closest_bats
        self.battery = None
        self.wire = None

    def connect(self, battery):
        self.battery = battery

    def add_wire(self, wire):
        self.wire = wire

        