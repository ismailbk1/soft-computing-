import math
import copy
import sys
import time
from matplotlib import pyplot as plt


# Function to calculate Euclidean distance between two points
def euclidean_distance(coords1, coords2):
    return math.sqrt((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2)

# Read instance data from file
def read_instance(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Extract necessary information
    dimension = 0
    capacity = 0
    node_coords = {}
    demands = {}
    num_trucks = 0
    optimal_value = 0

    for line in lines:
        if line.startswith("DIMENSION"):
            dimension = int(line.split()[-1])
        elif line.startswith("CAPACITY"):
            capacity = int(line.split()[-1])
        elif line.startswith("NODE_COORD_SECTION"):
            for _ in range(dimension):
                node, x, y = map(int, lines[lines.index(line) + 1 + _].split())
                node_coords[node] = (x, y)
        elif line.startswith("DEMAND_SECTION"):
            for _ in range(dimension):
                node, demand = map(int, lines[lines.index(line) + 1 + _].split())
                demands[node] = demand
        elif "COMMENT" in line:
            parts = line.split(',')
            for part in parts:
                if "No of trucks" in part:
                    num_trucks = int(part.split(':')[-1].strip())
                elif "Optimal value" in part:
                    optimal_str = part.split(':')[-1].strip()
                    optimal_value = int(''.join(filter(str.isdigit, optimal_str)))

    return dimension, capacity, node_coords, demands, num_trucks, optimal_value

# Calculate distance matrix
def calculate_distance_matrix(node_coords):
    distance_matrix = {}
    for node1, coord1 in node_coords.items():
        distance_matrix[node1] = {}
        for node2, coord2 in node_coords.items():
            distance_matrix[node1][node2] = euclidean_distance(coord1, coord2)
    return distance_matrix

# Calculate total route distance
def calculate_route_distance(route, distance_matrix):
    route_distance = 0
    for i in range(len(route) - 1):
        node1, node2 = route[i], route[i + 1]
        route_distance += distance_matrix[node1][node2]
    return route_distance

# Calculate total cost of the solution
def calculate_solution_cost(solution, distance_matrix):
    total_cost = 0
    for route in solution:
        total_cost += calculate_route_distance(route, distance_matrix)
    return total_cost

# Check if the solution satisfies capacity constraints
def check_capacity_constraint(solution, demands, capacity):
    for route in solution:
        route_demand = sum(demands[node] for node in route)
        if route_demand > capacity:
            return False
    return True

# Local search algorithm
def two_opt(route, i, j):
    new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
    return list(new_route)

# Local search algorithm
def local_search(instance_file, max_iterations=1000):
    start_time = time.time()  # Record the start time

    # Read instance data
    dimension, capacity, node_coords, demands, num_trucks, optimal_value = read_instance(instance_file)
    distance_matrix = calculate_distance_matrix(node_coords)

    # Initialize cost history
    cost_history = []

    # Initial solution (split nodes into routes based on capacity and demands)
    remaining_nodes = list(range(1, dimension + 1))
    num_vehicles = len([demand for demand in demands.values() if demand > 0])
    routes = []
    for _ in range(num_vehicles):
        route = []
        capacity_left = capacity
        for node in remaining_nodes:
            if demands[node] <= capacity_left:
                route.append(node)
                capacity_left -= demands[node]
        routes.append(route)
        for node in route:
            remaining_nodes.remove(node)

    best_solution = copy.deepcopy(routes)
    best_cost = calculate_solution_cost(best_solution, distance_matrix)

    # Add initial cost to history
    cost_history.append(best_cost)

    # Ensure the number of routes matches the number of trucks
    if len(best_solution) > num_trucks:
        best_solution = best_solution[:num_trucks]
    elif len(best_solution) < num_trucks:
        while len(best_solution) < num_trucks:
            best_solution.append([])

    iterations = 0
    while iterations < max_iterations:
        improved = False
        for i in range(num_vehicles):
            for j in range(i + 1, num_vehicles):
                if j >= len(best_solution):
                    continue  # Skip if j is out of range
                for k in range(len(best_solution[i])):
                    for l in range(len(best_solution[j])):
                        if l >= len(best_solution[j]):
                            continue  # Skip if l is out of range
                        new_solution_i = two_opt(best_solution[i], k, len(best_solution[i]) - 1)
                        new_solution_j = two_opt(best_solution[j], 0, l)
                        new_solution = best_solution[:i] + [new_solution_i] + best_solution[i + 1:j] + [
                            new_solution_j] + best_solution[j + 1:]
                        if check_capacity_constraint(new_solution, demands, capacity):
                            current_cost = calculate_solution_cost(best_solution, distance_matrix)
                            new_cost = calculate_solution_cost(new_solution, distance_matrix)
                            if new_cost < current_cost:
                                best_solution = copy.deepcopy(new_solution)
                                improved = True
        if not improved:
            break
        iterations += 1

        # Track the cost at each iteration
        current_cost = calculate_solution_cost(best_solution, distance_matrix)
        cost_history.append(current_cost)

    # Record the end time
    end_time = time.time()
    execution_time = end_time - start_time

    # Print the execution time
    print(f"Execution Time: {execution_time} seconds")

    # Plot the cost history
    plt.plot(cost_history, marker='o')
    plt.title('Cost Variation During Local Search')
    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.show()

    return best_solution
# Usage
instance_file = 'Instance1.txt'
best_solution = local_search(instance_file)
best_cost = calculate_solution_cost(best_solution, calculate_distance_matrix(read_instance(instance_file)[2]))

# Generate the output file name based on the instance file
output_file = f"output{instance_file.split('Instance')[1]}"
sys.stdout = open(output_file, "w")

# Print the best solution and its cost
route_strings = []
for i, route in enumerate(best_solution, start=1):
    route_string = f"Route #{i}: {' '.join(map(str, route))}"
    route_strings.append(route_string)

print('\n'.join(route_strings))
print(f"Cost: {best_cost}")

# Close the file to flush the output
sys.stdout.close()

# Reset stdout to the default value after redirection
sys.stdout = sys.__stdout__
