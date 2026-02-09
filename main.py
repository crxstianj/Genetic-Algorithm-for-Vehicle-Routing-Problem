import os
from datetime import datetime
import csv
from vrp.parser import parse_vrp_file
from vrp.split import split
from vrp.operators import *
from vrp.plot import plot_routes, plot_fitness
import numpy as np
from config import *

# Cargar datos
data = parse_vrp_file('data/A045-03f.dat')
depot = data['dimension'] - 1
num_customers = data['dimension'] - 1

# Inicializar población mixta (50% aleatoria, 50% Nearest Neighbor)
population = initialize_mixed_population(POP_SIZE, num_customers, data['distance_matrix'])

best_fitness = float('inf')
best_solution = None
fitness_history = []

# Evolución
for gen in range(GENERATIONS):
    fitness = []
    solutions = []

    for ind in population:
        cost, routes = split(ind, data['demands'], data['distance_matrix'], depot, data['capacity'], data['vehicles'])

        # Penalización por inviabilidad
        if cost == float('inf'):
            cost = 1e6 + sum(data['demands'][i] for i in ind)
        else:
            routes = or_opt_1(routes, data['distance_matrix'], data['demands'], data['capacity'], depot)

        fitness.append(cost)
        solutions.append(routes)

        if cost < best_fitness:
            best_fitness = cost
            best_solution = routes

    fitness_history.append(best_fitness)

    # Elitismo
    elite_idx = np.argmin(fitness)
    elite = population[elite_idx][:]

    new_population = [elite]

    while len(new_population) < POP_SIZE:
        p1 = tournament_selection(population, fitness, TOURNAMENT_SIZE)
        p2 = tournament_selection(population, fitness, TOURNAMENT_SIZE)

        if np.random.rand() < CROSSOVER_RATE:
            c1, c2 = ox_crossover(p1, p2)
        else:
            c1, c2 = p1[:], p2[:]

        # Mutaciones combinadas
        for c in [c1, c2]:
            if np.random.rand() < 0.5:
                scramble_mutation(c, MUTATION_RATE)
            else:
                swap_mutation(c, MUTATION_RATE)

        # Aplicar Or-opt si es factible
        for child in [c1, c2]:
            cost, routes = split(child, data['demands'], data['distance_matrix'], depot, data['capacity'], data['vehicles'])

            if cost != float('inf'):
                improved_routes = or_opt_1(routes, data['distance_matrix'], data['demands'], data['capacity'], depot)
                new_ind = [customer for route in improved_routes for customer in route]
                new_population.append(new_ind)
            else:
                new_population.append(child)

    population = new_population[:POP_SIZE]

    if gen % 1 == 0:
        print(f"Generación {gen + 1}: Mejor fitness = {best_fitness:.2f}")

# Resultados
print(f"\nDistancia total: {best_fitness:.2f}")
for i, route in enumerate(best_solution):
    route_demand = sum(data['demands'][customer] for customer in route)
    route_cost = sum(data['distance_matrix'][route[j]][route[j + 1]] for j in range(len(route) - 1)) \
                 + data['distance_matrix'][depot][route[0]] + data['distance_matrix'][route[-1]][depot]
    print(f"Ruta {i + 1}: {' -> '.join(map(str, [depot] + route + [depot]))} | Costo: {route_cost:.2f} | Demanda: {route_demand}")


os.makedirs("results", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"results/fitness_{timestamp}.csv"

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Generación", "Fitness"])
    for i, fit in enumerate(fitness_history, 1):
        writer.writerow([i, fit])

print(f"\nHistorial de fitness guardado en: {filename}")

# Gráficas
plot_fitness(fitness_history)
plot_routes(best_solution, depot, data['demands'])
