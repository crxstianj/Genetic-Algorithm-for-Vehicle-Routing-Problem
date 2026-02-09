from vrp.parser import parse_vrp_file

# Cargar datos
data = parse_vrp_file('data/A045-03f.dat')
demands = data['demands']
dist = data['distance_matrix']
depot = 44

# Ruta capturada (sin depósito)
best_solution = [
    [4, 5, 0, 31, 30, 29, 24, 42, 23, 22, 18, 16, 21, 1, 2],               # Ruta 1
    [3, 41, 6, 10, 43, 11, 12, 13, 15, 17, 14, 19, 20, 7, 9, 8, 40, 39],   # Ruta 2
    [38, 35, 32, 28, 25, 26, 27, 33, 34, 36, 37]                           # Ruta 3
]

# Calcular costo y demanda de cada ruta
for i, route in enumerate(best_solution):
    demand = sum(demands[n] for n in route)
    cost = dist[depot][route[0]] + sum(dist[route[j]][route[j + 1]] for j in range(len(route) - 1)) + dist[route[-1]][depot]
    print(f"Ruta {i + 1}: {' -> '.join(map(str, [depot] + route + [depot]))}")
    print(f"  Costo: {cost:.2f}")
    print(f"  Demanda: {demand}\n")
