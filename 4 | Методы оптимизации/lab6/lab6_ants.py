import numpy as np
import random

INF = float('inf')

graph = [
    [INF, 3, 14, INF, 6, INF, INF],
    [3, INF, INF, 13, INF, INF, 35],
    [14, INF, INF, INF, INF, 8, INF],
    [INF, 13, INF, INF, 16, 8, 6],
    [6, INF, INF, 16, INF, 9, INF],
    [INF, INF, 8, 8, 9, INF, 21],
    [INF, 35, INF, 6, INF, 21, INF]
]

num_nodes = len(graph)
start_node = 0
end_node = 6

ALPHA = 1.0  # Влияние феромона (стадный инстинкт)
BETA = 2.0  # Влияние расстояния (эвристика/жадность)
EVAPORATION = 0.5  # Скорость испарения феромона
Q = 100  # Константа оставляемого феромона
ANTS_COUNT = 10  # Количество муравьев
ITERATIONS = 50  # Количество итераций

pheromones = np.ones((num_nodes, num_nodes)) * 0.1

best_path = None
best_distance = INF

for iteration in range(ITERATIONS):
    paths = []
    distances = []

    for ant in range(ANTS_COUNT):
        current_node = start_node
        path = [current_node]
        distance = 0
        visited = set([current_node])
        dead_end = False

        while current_node != end_node:
            available_nodes = [n for n in range(num_nodes)
                               if graph[current_node][n] != INF and n not in visited]

            if not available_nodes:
                dead_end = True
                break

            probabilities = []
            for next_node in available_nodes:
                tau = pheromones[current_node][next_node] ** ALPHA
                eta = (1.0 / graph[current_node][next_node]) ** BETA
                probabilities.append(tau * eta)

            prob_sum = sum(probabilities)
            if prob_sum == 0:
                dead_end = True
                break

            probabilities = [p / prob_sum for p in probabilities]

            next_node = random.choices(available_nodes, weights=probabilities)[0]

            path.append(next_node)
            distance += graph[current_node][next_node]
            visited.add(next_node)
            current_node = next_node

        if not dead_end:
            paths.append(path)
            distances.append(distance)
            if distance < best_distance:
                best_distance = distance
                best_path = path

    pheromones *= (1 - EVAPORATION)

    for i in range(len(paths)):
        path = paths[i]
        dist = distances[i]
        pheromone_to_add = Q / dist

        for j in range(len(path) - 1):
            from_node = path[j]
            to_node = path[j + 1]
            pheromones[from_node][to_node] += pheromone_to_add
            pheromones[to_node][from_node] += pheromone_to_add

node_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

if best_path:
    best_path_names = [node_names[n] for n in best_path]
    print(f"Лучший маршрут: {' -> '.join(best_path_names)}")
    print(f"Длина маршрута: {best_distance}")
else:
    print("Не удалось найти путь. Проверьте связи в графе.")