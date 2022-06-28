from path_finders import hor_vert_pathfinder
from sklearn import cluster, metrics
from classes.batteries import Battery, Batteries
from classes.houses import House, Houses
from classes.wires import Wire, Wires
from visualize import visualize_grid


def generate_clusters(batteries):
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
            path = hor_vert_pathfinder(node, cluster)
            wire_paths.append((battery.id, path))
            wire_branches.append(set(path))

        # path gets drawn from the battery to its clusters
        for cluster in cluster_centers:
            path = hor_vert_pathfinder(battery.position, cluster)
            wire_paths.append((battery.id, path))
    
    return wire_branches, wire_paths

def select_cluster_centers(nodes):
    """
    divides houses over clusters in a most efficient way
    """
    highest_score = -1

    # generate silhouette scores and cluster_centers for k = 2-11
    for k in range(2, 10):
        kmeans = cluster.KMeans(n_clusters = k).fit(nodes)
        labels = kmeans.labels_
        silhouette_score = metrics.silhouette_score(nodes, labels, metric = 'euclidean')
        if silhouette_score > highest_score:
            highest_score = silhouette_score
            cluster_centers = kmeans.cluster_centers_
    
    return cluster_centers.astype(int)
    
def get_cluster(node, cluster_centers, battery):
    """selects the best supernode for a node, or chooses the battery to connect to"""
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


if __name__ == "__main__":

    wijk_num = 2
    class_directory = f'../data/district_{wijk_num}/district-{wijk_num}_'

    houses = Houses(class_directory + 'houses.csv')
    batteries = Batteries(class_directory + 'batteries.csv')
    wires = Wires("hor_ver")

    grid = False
    while grid == False:
        grid = wires.generate(houses, batteries)
    
    wire_branches, wire_paths = generate_clusters(batteries)

    # calculate cost and print it
    total_cost = 0
    for branch in wire_branches:
        total_cost += (len(branch) - 1) * 9
    total_cost += 5 * 5000
    print(total_cost)

    visualize_grid(houses.get_members(),
        batteries.get_members(),
        wire_paths, 'test_grid.png')
