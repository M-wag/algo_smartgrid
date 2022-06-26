# hierachial steiner point heuristic program

from path_finders import hor_vert_pathfinder


def generate_steiner(houses, batteries):

    # divide the houses over all batteries
    divide_houses(houses, batteries)

    # generates a hierarchial steiner tree per battery
    for battery in batteries.get_members():
        wire_paths = []
        wire_set = set()

        # stage 0 contains all house coordinates
        nodes = [coordinates for house.position in battery.houses.values()]

        # continues until only the battery remains
        while len(nodes) != 1:
            
            # supernodes get selected and removed from the nodes list
            nodes, supernodes= select_supernodes(nodes)
            
            # all nodes get connected to their respective supernode
            for node in nodes:
                supernode = get_supernode(node, supernodes, battery)
                path = hor_vert_pathfinder(node, supernode)
                wire_paths.append(path)
                wire_set = wire_set & set(path)

            # the old supernodes become the new nodes in the next tier
            nodes = supernodes
    
    return wire_set, wire_paths

def divide_houses(houses, batteries):
    """
    divides houses over the batteries in a most efficient way
    without exceeding the capacities
    """
    #TODO: define the most efficient way of packing,
    #      for use in the steiner tree generator

    # then appends all appointed houses to their respective 
    # batteries "assigned_houses" list

def select_supernodes(nodes):
    """selects which nodes will become the new super nodes"""
    supernodes = []

    #TODO: find a good way of assigning supernodes
    #      amount of supernodes should be calculated too

    return nodes, supernodes

def get_supernode(node, supernodes, battery):
    """selects the best supernode for a node, or chooses the battery to connect to"""
    closest_supernode = None
    lowest_distance = 9999

    # finds the closest supernode to connect to
    for supernode in supernodes:
        
        # manhattan distance
        distance = abs(node[0] - supernode[0]) + abs(node[1] - supernode[1])

        if distance < lowest_distance:
            lowest_distance = distance
            closest_supernode = supernode

    # if battery is closer than the nearest supernode, connect to the battery
    batt_x, batt_y = battery.position
    distance_to_battery = abs(node[0] - batt_x[0]) + abs(node[1] - batt_y[1])
    if distance_to_battery < lowest_distance:
        closest_supernode = battery.position

    return closest_supernode
