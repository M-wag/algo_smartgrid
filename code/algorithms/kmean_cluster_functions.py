import numpy as np
from .path_finders import hor_vert_pathfinder, straight_pathfinder
from sklearn import cluster, metrics


def cluster_swap(battery_1, house_1, battery_2, house_2):
    '''
    Swaps two houses in a grid, changing all internal values associated

            Parameters:
                    battery_1 (Battery):
                        A class representing a battery, connected to house_1
                    house_1 (House):
                        A class representing a house, connected to battery_1
                    battery_2 (Battery):
                        A class representing a battery, connected to house_2
                    house_2 (House):
                        A class representing a house, connected to battery_2

            Returns:
                    True for success, False otherwise.
    '''

    if battery_1.id == battery_2.id:
        return False

    if not battery_1.can_connect(house_2.max_output - house_1.max_output):
        return False
    
    if not battery_2.can_connect(house_1.max_output - house_2.max_output):
        return False

    battery_1.disconnect(house_1)
    battery_2.disconnect(house_2)

    battery_1.connect(house_2)
    battery_2.connect(house_1)

    return True


def random_house_batt_pair(batteries):
    '''
    Chooses a random house, battery pair

            Parameters:
                    batteries (Batteries):
                        A class containing Battery classes

            Returns:
                    battery (Battery):
                        A class representing a Battery
                    house (House):
                        A class representing a House
    '''

    battery = np.random.choice(list(batteries.get_members()))
    house = np.random.choice(list(battery.houses.values()))

    return battery, house


def pick_and_swap(batteries):
    '''
    Picks two houses and swaps them, until a valid setup is found

            Parameters:
                    batteries (Batteries):
                        A class containing Battery classes

            Returns:
                    battery_1 (Battery):
                        A class representing a battery, connected to house_1
                    house_1 (House):
                        A class representing a house, connected to battery_1
                    battery_2 (Battery):
                        A class representing a battery, connected to house_2
                    house_2 (House):
                        A class representing a house, connected to battery_2
    '''
    swapped = False
    while swapped == False:
        battery_1, house_1 = random_house_batt_pair(batteries)
        battery_2, house_2 = random_house_batt_pair(batteries)
        swapped = cluster_swap(battery_1, house_1, battery_2, house_2)
    
    return battery_1, house_1, battery_2, house_2


def generate_clusters(batteries, type_wires):
    '''
    Generates clusters per battery and calculates their paths

            Parameters:
                    batteries (Batteries):
                        A class containing Battery classes
                    type_wires ("string"):
                        The wire pathfinding type

            Returns:
                    wire_branches (Set[Tuple[int, int]]):
                        A set of all wire coordinates over all batteries
                    wire_paths (list[List[Tuple[int, int]]):
                        A list of all wire-paths and their coordinates
    '''

    wire_paths = []
    wire_branches = []
    for battery in batteries.get_members():

        nodes = [house.position for house in battery.houses.values()]

        # clusters get selected
        cluster_centers = select_cluster_centers(nodes)
        
        # all nodes get connected to their respective cluster_center
        for node in nodes:

            # cluster is chosen based on distance
            cluster = get_cluster(node, cluster_centers, battery)
            if type_wires == "hor_ver":
                path = hor_vert_pathfinder(node, cluster)
            else:
                path = straight_pathfinder(node, cluster)
            wire_paths.append((battery.id, path))
            wire_branches.append(set(path))

        # path gets drawn from the battery to its clusters
        for cluster in cluster_centers:
            if type_wires == "hor_ver":
                path = hor_vert_pathfinder(battery.position, cluster)
            else:
                path = straight_pathfinder(battery.position , cluster)
            wire_paths.append((battery.id, path))
    
    return wire_branches, wire_paths


def select_cluster_centers(nodes):
    '''
    Calculates the cluster centers for a set of coordinates,
    amount of clusters ranges between 3 and 7

    The cluster amount is chosen by the highest silhouette-score

            Parameters:
                    nodes (List[Tuple[int, int]]):
                        A list of coordinates

            Returns:
                    cluster_centers (List[Tuple[int, int]]):
                        A list of the chosen cluster center coordinates
    '''

    highest_score = -1

    # generate silhouette scores and cluster_centers for k = 3-6
    for k in range(3, 7):
        kmeans = cluster.KMeans(n_clusters = k).fit(nodes)
        labels = kmeans.labels_
        silhouette_score = metrics.silhouette_score(nodes, labels, metric = 'euclidean')
        if silhouette_score > highest_score:
            highest_score = silhouette_score
            cluster_centers = kmeans.cluster_centers_
    
    return cluster_centers.astype(int)
    

def get_cluster(node, cluster_centers, battery):
    '''
    Selects the closest cluster or battery per node

            Parameters:
                    node (Tuple[int, int]):
                        coordinates of a node
                    cluster_centers (List[Tuple[int, int]]):
                        A list of cluster center coordinates
                    battery (Battery):
                        A class representing a battery

            Returns:
                    closest_cluster (Tuple[int, int]):
                        The chosen cluster or battery coordinates
    '''

    lowest_distance = 9999

    # finds the closest cluster to connect to
    for cluster in cluster_centers:
        
        # manhattan distance
        distance = abs(node[0] - cluster[0]) + abs(node[1] - cluster[1])

        if distance < lowest_distance:
            lowest_distance = distance
            closest_cluster = cluster

    # if battery is closer than the nearest cluster, connect to the battery
    batt_x, batt_y = battery.position
    distance_to_battery = abs(node[0] - batt_x) + abs(node[1] - batt_y)
    if distance_to_battery < lowest_distance:
        closest_cluster = battery.position

    return closest_cluster
