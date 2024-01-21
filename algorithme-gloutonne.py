trucks = None
optimal_value = None
capacity = None
dimension = None
nodes = []
customers = []
deposit_node = None

# read variables from input text file

def read_input(file_path):
    global trucks, optimal_value, capacity, dimension
    with open(file_path, 'r') as file:
        lines = file.readlines()

    process_coordinates = False
    process_demands = False

    for line in lines:
        if(line.startswith('COMMENT')):
            sentences = line.split(',')
            trucks = int(sentences[1].split(': ')[1])
            optimal_value = int(sentences[2].strip().split(': ')[1][0:-1])
        elif(line.startswith('DIMENSION')):
            dimension = int(line.split(' : ')[1])
        elif(line.startswith('CAPACITY')):
            capacity = int(line.split(' : ')[1])
        elif(line.startswith('NODE_COORD_SECTION')):
            process_coordinates = True
        elif(process_coordinates):
            id, x, y = list(map(int,line.strip().split(' ')))
            nodes.append([id, x, y])
            if(len(nodes) == dimension):
                process_coordinates = False

        elif(line.startswith('DEMAND_SECTION')):
            process_demands = True
        elif(process_demands):
            id, demand = list(map(int,line.strip().split(' ')))
            for node in enumerate(nodes):
                if node[0] == id - 1:
                    nodes[id - 1].append(demand)
            if(id == dimension):
                process_demands = False
                

read_input('./input1.txt')
deposit_node = nodes[0]
customers = nodes[1:]

# import libraries
import numpy as np
import math
import time

# initialize variables
routes = [[] for _ in range(trucks)]
loads = [0 for _ in range(trucks)]
visited = [False for _ in range(len(nodes))]
visited[0] = True
total_cost = 0

# calculate the distance between two nodes
def distance(node1, node2):
    return np.sqrt((node1[1] - node2[1])**2 + (node1[2] - node2[2])**2)

#find the nearest neighbor of a node
def nearest_neighbor(node):
    min_dist = math.inf
    min_index = -1
    for j in range(len(nodes)):
        if not visited[j] and distance(node, nodes[j]) < min_dist:
            min_dist = distance(node, nodes[j])
            min_index = j
    return min_index, min_dist


# measure execution time (START)
start_time = time.time()

# loop over all vehicles
for v in range(trucks):
    i = 0
    while True:
        j, d = nearest_neighbor(nodes[i])
        if j == -1:
            break
        if loads[v] + nodes[j][3] <= capacity:
            routes[v].append(j)
            loads[v] += nodes[j][3]
            visited[j] = True
            total_cost += d
            i = j
        else:
            total_cost += distance(nodes[i], nodes[0])
            i = 0
            break

# measure execution time (END)
end_time = time.time()

# print the solution and execution time
print("Total cost:", total_cost)
print("Optimal:  ", optimal_value)
print("Routes:")
for v in range(trucks):
    print(f"Route #{v+1}: 0 -> {' -> '.join(str(c) for c in routes[v])} -> 0")


# save results in text file
input_number = 1
output_filename = f"result{input_number}.txt"

with open(output_filename, 'w') as file:
    for v in range(trucks):
        file.write(f"Route #{v+1}: {' '.join(str(c) for c in routes[v][1:-1])}\n")
    file.write(f"Cost {total_cost}\n")

print("Execution time: {:.4f} seconds".format(end_time - start_time))