import matplotlib.pyplot as plt

def plot_routes(routes, depot, demands, coords=None):
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r', 'c', 'm', 'y']

    for idx, route in enumerate(routes):
        if not route:
            continue
        full_route = [depot] + route + [depot]
        x, y = [], []
        for node in full_route:
            if coords:
                x.append(coords[node][0])
                y.append(coords[node][1])
            else:
                x.append(node % 10)
                y.append(node // 10)

        plt.plot(x, y, marker='o', color=colors[idx % len(colors)], linestyle='-', label=f'Ruta {idx + 1}')
        plt.scatter([x[0]], [y[0]], marker='s', s=100, c='k', label='Depósito' if idx == 0 else "")
        for i, node in enumerate(full_route[1:-1]):
            plt.text(x[i + 1], y[i + 1], f'{node}\n{demands[node]}', fontsize=8)

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Rutas de Vehículos')
    plt.legend()
    plt.grid(False)
    plt.show()


def plot_fitness(fitness_history):
    plt.figure(figsize=(10, 5))
    plt.plot(fitness_history, color='blue')
    plt.title('Evolución del Fitness')
    plt.xlabel('Generación')
    plt.ylabel('Mejor Fitness')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
