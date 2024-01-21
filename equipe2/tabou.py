import random
import copy
import time

class CVRPInstance:
    def __init__(self, filename):
        self.load_instance(filename)

    def load_instance(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        self.dimension = int(self.get_value(lines, 'DIMENSION'))
        self.capacity = int(self.get_value(lines, 'CAPACITY'))
        self.coords = self.read_section(lines, 'NODE_COORD_SECTION', self.dimension)
        self.demands = self.read_section(lines, 'DEMAND_SECTION', self.dimension)
        depot_value = self.get_value(lines, 'DEPOT_SECTION')
        if depot_value is not None:
            self.depot = int(depot_value.split()[0])

    def get_value(self, lines, key):
        for line in lines:
            if key in line:
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip()
                else:
                    return None
        return None

    def read_section(self, lines, section_key, size):
        section_start = lines.index(f'{section_key} \n') + 1
        section_end = section_start + size
        section = [list(map(int, line.split()[1:])) for line in lines[section_start:section_end]]
        return section

class CVRPSolution:
    def __init__(self, instance):
        self.instance = instance
        self.routes = [[] for _ in range(instance.dimension)]
        self.best_solution = None
        self.best_cost = float('inf')

    def initialize_solution(self):
        customers = list(range(1, self.instance.dimension + 1))
        random.shuffle(customers)

        route_index = 0
        current_demand = 0
        for customer in customers:
            if current_demand + self.instance.demands[customer - 1][0] > self.instance.capacity:
                route_index += 1
                current_demand = 0
            self.routes[route_index].append(customer)
            current_demand += self.instance.demands[customer - 1][0]

    def calculate_route_cost(self, route):
        cost = 0

        if not route:
            return cost

        for customer in route:
            if 1 <= customer <= self.instance.dimension:
                cost += self.instance.coords[customer - 1][1]  # Coordonnée y

        return cost

    def calculate_total_cost(self):
        total_cost = 0
        for route in self.routes:
            total_cost += self.calculate_route_cost(route)
        return total_cost

    def move_customer(self, route_index, customer_index, new_route_index):
        customer = self.routes[route_index].pop(customer_index)
        self.routes[new_route_index].append(customer)

    def apply_tabu_search(self, iterations, tabu_list_size):
        start_time = time.time()
        tabu_list = []

        for _ in range(iterations):
            for route_index in range(len(self.routes)):
                if len(self.routes[route_index]) > 1:
                    for customer_index in range(len(self.routes[route_index])):
                        for new_route_index in range(len(self.routes)):
                            if route_index != new_route_index:
                                candidate_solution = copy.deepcopy(self)
                                candidate_solution.move_customer(route_index, customer_index, new_route_index)
                                candidate_cost = candidate_solution.calculate_total_cost()

                                if candidate_cost < self.best_cost and (route_index, customer_index, new_route_index) not in tabu_list:
                                    self.best_solution = copy.deepcopy(candidate_solution)
                                    self.best_cost = candidate_cost
                                    tabu_list.append((route_index, customer_index, new_route_index))
                                    if len(tabu_list) > tabu_list_size:
                                        tabu_list.pop(0)

        self.routes = self.best_solution.routes
        end_time = time.time()
        execution_time = end_time - start_time
        self.execution_time = execution_time

    def print_solution(self, filename):
        with open(filename, 'w') as file:
            for i, route in enumerate(self.routes, start=1):
                if route:
                    file.write(f"Route #{i}: {' '.join(map(str, route))}\n")
            file.write(f"Cost {self.calculate_total_cost()}\n")
            file.write(f"Execution Time: {self.execution_time} seconds\n")
        print(f"Solution printed to {filename}")

if __name__ == "__main__":
    instance_file = "B-n78-k10.txt"
    output_file = "B-n78-k10-output.txt"

    instance = CVRPInstance(instance_file)
    best_solution = None
    best_cost = float('inf')

    for _ in range(10):
        solution = CVRPSolution(instance)
        solution.initialize_solution()
        solution.apply_tabu_search(iterations=40, tabu_list_size=5)  # Adjust the number of iterations and tabu list size as needed

        current_cost = solution.calculate_total_cost()
        if current_cost < best_cost:
            best_solution = copy.deepcopy(solution)
            best_cost = current_cost

        if best_solution is not None:
            best_solution.print_solution(output_file)
