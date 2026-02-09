from config import PENALTY_FACTOR

def split(individual, demands, distance_matrix, depot, capacity, num_vehicles):
    routes = []
    route = []
    load = 0
    total_distance = 0
    used_vehicles = 0
    i = 0

    while i < len(individual):
        customer = individual[i]
        demand = demands[customer]

        if load + demand <= capacity:
            route.append(customer)
            load += demand
            i += 1
        else:
            if route:
                routes.append(route)
                total_distance += compute_route_distance(route, depot, distance_matrix)
                used_vehicles += 1
            route = []
            load = 0

    if route:
        routes.append(route)
        total_distance += compute_route_distance(route, depot, distance_matrix)
        used_vehicles += 1

    # Penalizar si excede número de vehículos
    if used_vehicles > num_vehicles:
        total_distance += (used_vehicles - num_vehicles) * PENALTY_FACTOR

    # Penalización proporcional al exceso de capacidad
    for r in routes:
        route_demand = sum(demands[c] for c in r)
        if route_demand > capacity:
            total_distance += (route_demand - capacity) * PENALTY_FACTOR

    return total_distance, routes


def compute_route_distance(route, depot, distance_matrix):
    path = [depot] + route + [depot]
    return sum(distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))
