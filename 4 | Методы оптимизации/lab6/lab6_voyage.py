import random

dist_matrix = [
    [0, 5, 11, 5, 4],
    [5, 0, 4, 8, 9],
    [11, 4, 0, 9, 9],
    [5, 8, 9, 0, 6],
    [4, 9, 9, 6, 0]
]

POPULATION_SIZE = 4
MUTATION_RATE = 0.01
GENERATIONS = 50


def fitness(chromosome):
    dist = 0
    for i in range(len(chromosome) - 1):
        dist += dist_matrix[chromosome[i]][chromosome[i + 1]]
    dist += dist_matrix[chromosome[-1]][chromosome[0]]
    return dist


def init_population():
    pop = []
    base = [0, 1, 2, 3, 4]
    for _ in range(POPULATION_SIZE):
        shuffled = base.copy()
        random.shuffle(shuffled)
        pop.append(shuffled)
    return pop


def universal_crossover(donor_for_fill, donor_for_fragment, cut_start, cut_end):
    n = len(donor_for_fill)
    child = [-1] * n

    for i in range(cut_start, cut_end + 1):
        child[i] = donor_for_fragment[i]

    start_idx = (cut_start + 1) % n

    fill_order = []
    for i in range(n):
        idx = (start_idx + i) % n
        if donor_for_fill[idx] not in child:
            fill_order.append(donor_for_fill[idx])

    insert_idx = 0
    for val in fill_order:
        while child[insert_idx] != -1:
            insert_idx += 1
        child[insert_idx] = val

    return child


def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        idx1, idx2 = random.sample(range(len(chromosome)), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome


population = init_population()

for gen in range(GENERATIONS):
    population.sort(key=fitness)

    p1 = population[0]
    p2 = population[1]

    cut_start = random.randint(0, len(p1) - 2)
    cut_end = random.randint(cut_start + 1, len(p1) - 1)

    child1 = universal_crossover(p1, p2, cut_start, cut_end)
    child2 = universal_crossover(p2, p1, cut_start, cut_end)

    child1 = mutate(child1)
    child2 = mutate(child2)

    population.extend([child1, child2])
    population.sort(key=fitness)
    population = population[:POPULATION_SIZE]

    print(f"Итерация {gen + 1}: Лучший путь = {[x + 1 for x in population[0]]}, Дистанция = {fitness(population[0])}")

print(f"\nОптимальный найденный путь: {[x + 1 for x in population[0]]}")
print(f"Сумма расстояний: {fitness(population[0])}")