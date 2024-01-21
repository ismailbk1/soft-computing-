import json

def convert_to_routes(json_data):
    runs = json_data["RUNS"]
    best_run = json_data["BEST_RUN"]

    best_run_data = runs[best_run]
    best_individual = best_run_data["best_individual"]

    problem_info = (
        f"problem_set_name: {best_run_data['problem_set_name']}, "
        f"time: {best_run_data['time']}, "
        f"generations: {best_run_data['generations']}, "
        f"cxpb: {best_run_data['cxpb']}, "
        f"mutpb: {best_run_data['mutpb']}, "
        f"cx_algorithm: {best_run_data['cx_algorithm']}, "
        f"mut_algorithm: {best_run_data['mut_algorithm']}, "
        
    )

    routes = [problem_info]
    
    for route_number, route_data in best_individual.items():
        nodes = [node["_node"] for node in route_data]
        route_str = f"Route #{route_number}: {' '.join(map(str, nodes))}"
        routes.append(route_str)

    cost = best_run_data["best_individual_fitness"]
    routes.append(f"Cost {cost}")

    return '\n'.join(routes)

# Load your JSON data
with open('./cycle_xo_50000_0.85_B-n78-k10__20240121__04_38_19PM.json', 'r') as file:
    json_data = json.load(file)

# Convert to routes format
result = convert_to_routes(json_data)

# Print or save the result
print(result)

# If you want to save the result to a file
with open('output_routes75.txt', 'w') as output_file:
    output_file.write(result)
