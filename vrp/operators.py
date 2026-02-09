import random

#SE PROBARON MULTIPLES COMBINACIONES, FINALMENTE SE UTILIZAN LAS QUE
# OBTUVIERON MEJORES RESULTADOS

def initialize_population(pop_size, num_customers):
    return [random.sample(range(num_customers), num_customers) for _ in range(pop_size)]

def initialize_individual(num_customers):
    individual = list(range(num_customers))
    random.shuffle(individual)
    return individual

def nearest_neighbor_solution(distance_matrix, depot, num_customers):
    unvisited = list(range(num_customers))
    current = depot
    tour = []

    while unvisited:
        nearest = min(unvisited, key=lambda x: distance_matrix[current][x])
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return tour

def initialize_mixed_population(pop_size, num_customers, distance_matrix):
    half = pop_size // 2
    depot = num_customers
    population = [initialize_individual(num_customers) for _ in range(half)]
    population += [nearest_neighbor_solution(distance_matrix, depot, num_customers) for _ in range(pop_size - half)]
    return population


def ox_crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child1 = [-1] * size
    child2 = [-1] * size

    for i in range(a, b + 1):
        child1[i] = parent1[i]
        child2[i] = parent2[i]

    fill_child(parent2, child1, b, a)
    fill_child(parent1, child2, b, a)
    return child1, child2

def pmx_crossover(parent1, parent2):
    size = len(parent1)
    p1, p2 = parent1[:], parent2[:]

    cx_point1 = random.randint(0, size - 2)
    cx_point2 = random.randint(cx_point1 + 1, size - 1)

    def pmx(p1, p2):
        child = [None] * size
        child[cx_point1:cx_point2+1] = p1[cx_point1:cx_point2+1]

        for i in range(cx_point1, cx_point2 + 1):
            if p2[i] not in child:
                val = p2[i]
                idx = i
                while True:
                    val = p1[idx]
                    idx = p2.index(val)
                    if child[idx] is None:
                        child[idx] = p2[i]
                        break

        for i in range(size):
            if child[i] is None:
                child[i] = p2[i]
        return child

    return pmx(p1, p2), pmx(p2, p1)

def fill_child(parent, child, start, end):
    size = len(child)
    ptr = (start + 1) % size
    for gene in parent:
        if gene not in child:
            while child[ptr % size] != -1:
                ptr = (ptr + 1) % size
            child[ptr % size] = gene
            ptr = (ptr + 1) % size

def swap_mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        a, b = random.sample(range(len(individual)), 2)
        individual[a], individual[b] = individual[b], individual[a]

def insertion_mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        if i < j:
            individual.insert(j, individual.pop(i))
        else:
            individual.insert(i, individual.pop(j))

def scramble_mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = sorted(random.sample(range(len(individual)), 2))
        subseq = individual[i:j+1]
        random.shuffle(subseq)
        individual[i:j+1] = subseq

def tournament_selection(population, fitness, k=5):
    selected = random.sample(range(len(population)), k)
    best_idx = min(selected, key=lambda i: fitness[i])
    return population[best_idx]

def or_opt_1(routes, distance_matrix, demands, capacity, depot):
    improved = True

    def route_distance(route):
        return sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))

    def route_demand(route):
        return sum(demands[customer] for customer in route)

    while improved:
        improved = False
        for r_idx, route in enumerate(routes):
            for i in range(len(route)):
                customer = route[i]
                for r2_idx, route2 in enumerate(routes):
                    for j in range(len(route2) + 1):
                        if r_idx == r2_idx and (j == i or j == i + 1):
                            continue

                        new_routes = [r[:] for r in routes]
                        new_routes[r_idx].remove(customer)
                        new_routes[r2_idx].insert(j, customer)

                        # Validar restricciones de capacidad
                        if route_demand(new_routes[r2_idx]) > capacity:
                            continue

                        # Calcular nuevo costo total
                        total_cost = sum(
                            route_distance([depot] + r + [depot]) for r in new_routes
                        )

                        current_cost = sum(
                            route_distance([depot] + r + [depot]) for r in routes
                        )

                        if total_cost < current_cost:
                            routes = new_routes
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
    return routes
