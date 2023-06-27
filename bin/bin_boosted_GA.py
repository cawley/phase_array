import sys
import time
from multiprocessing import Pool
from matplotlib import pyplot as plt

start = time.time()


def objective(individual):
    # Convert the list of bits to a 16x16 array of integers (each between 0 and 63)
    array = np.array(
        [
            int("".join(map(str, individual[i : i + BITS_PER_ENTRY])), 2)
            for i in range(0, len(individual), BITS_PER_ENTRY)
        ]
    ).reshape((ARRAY_SIZE, ARRAY_SIZE))
    # Calculate the objective function value
    value = np.var(array)
    return (value,)


def h(individual):
    array = np.array(individual)
    energy_matrix = 1 - array
    return (energy_matrix.sum(),)


from deap import base, creator, tools
import random
import numpy as np

# Problem constants
ARRAY_SIZE = 8  # Size of the phase array
BITS_PER_ENTRY = 6  # Number of bits per phase value

# Genetic Algorithm constants
POPULATION_SIZE = 100  # Number of individuals in population
CROSSOVER_PROB = 0.5  # Probability of crossover
# MUTATION_PROB = 0.5 # Probability of mutation
NGEN = 10000  # Number of generations

# Create types
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimization problem
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator: define how each entry (phase value) is created
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers: define how an individual and the population are created
toolbox.register(
    "individual",
    tools.initRepeat,
    creator.Individual,
    toolbox.attr_bool,
    ARRAY_SIZE * ARRAY_SIZE * BITS_PER_ENTRY,
)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operator registration: define the genetic operations
toolbox.register("evaluate", h)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

setup = time.time()
stime = setup - start


def main(MUTATION_PROB, CROSSOVER_PROB, POPULATION_SIZE):
    start = time.time()

    pop = toolbox.population(n=POPULATION_SIZE)

    best = pop[0]

    x = []
    y = []

    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    pool = Pool()
    elapsed = 0
    for g in range(NGEN):
        scores = pool.map(h, pop)

        sorted_population = [
            x for _, x in sorted(zip(scores, pop), key=lambda pair: pair[0])
        ]
        elite_cutoff = int(
            len(sorted_population) * 0.0625
        )  # This amounts to ~96 elite individuals (1/16)
        elite = sorted_population[:elite_cutoff]

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CROSSOVER_PROB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTATION_PROB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        offspring = offspring[: len(offspring) - elite_cutoff] + elite

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)

        for ind in pop:
            if h(ind) < h(best):
                best = ind
                x.append(g)
                y.append(h(best)[0])
                print(f">{g}: New Best Score: {h(best)} {best} ")

        if abs(best.fitness.values[0]) < 1e-9:
            end = time.time()
            elapsed = end - start
            print(
                f"Max Score Achieved after {elapsed} seconds on iteration {g} with: {best}"
            )
            g = NGEN
            break

        if abs(best.fitness.values[0]) >= 1e-9 and g == NGEN:
            end = time.time()
            elapsed = end - start
            print(
                f"TEST FAILED Best Score: {h(best)} after {elapsed} seconds and {g} iterations."
            )
            break
        pop[:] = offspring
    pool.close()
    return x, y, elapsed


# Run the algorithm
if __name__ == "__main__":
    mutation_probs = [0.4]
    crossover_probs = [0.1]
    pop_sizes = [10]
    results = []
    for mut_prob in mutation_probs:
        for cross_prob in crossover_probs:
            for pop_size in pop_sizes:
                print(
                    f"Running with: \n MUTATION_PROB = {mut_prob} \n CROSSOVER_PROB = {cross_prob} \n POPULATION_SIZE = {pop_size} \n"
                )
                x, y, e = main(mut_prob, cross_prob, pop_size)
                results.append((mut_prob, cross_prob, pop_size, x, y, e))

    fig, axs = plt.subplots(
        len(mutation_probs), 1, figsize=(10, len(mutation_probs) * 5)
    )
    for idx, (mut_prob, cross_prob, pop_size, x, y, elapsed) in enumerate(results):
        axs[idx].plot(x, y)
        axs[idx].set_title(f"Scores Across Generations (Mutation Prob: {mut_prob})")
        axs[idx].text(
            0.5,
            -0.1,
            f"Elapsed Time: {elapsed}",
            transform=axs[idx].transAxes,
            ha="right",
        )

    print(f"Setup time: {stime}")
    plt.tight_layout()
    plt.show()
