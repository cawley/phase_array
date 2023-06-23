import numpy as np

def h(individual):
    array = np.array(individual)
    expected = np.ones(individual.shape)
    energy_matrix = np.zeros(individual.shape)

    for i in range(len(energy_matrix)):
        energy_matrix[i] = 1 - array[i]

    return energy_matrix.sum

def h(individual):
    array = np.array(individual)
    expected = np.ones(individual.shape)
    energy_matrix = np.zeros(individual.shape)

    for i in range(len(energy_matrix)):
        energy_matrix[i] = 1 - array[i]

    return energy_matrix.sum()

from deap import base, creator, tools
import random
import numpy as np

# Problem constants
ARRAY_SIZE = 16  # Size of the phase array
BITS_PER_ENTRY = 6  # Number of bits per phase value

# Genetic Algorithm constants
POPULATION_SIZE = 100  # Number of individuals in population
CROSSOVER_PROB = 0.5  # Probability of crossover
MUTATION_PROB = 0.2  # Probability of mutation
NGEN = 50  # Number of generations

# Create types
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimization problem
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator: define how each entry (phase value) is created
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers: define how an individual and the population are created
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, ARRAY_SIZE * ARRAY_SIZE * BITS_PER_ENTRY)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operator registration: define the genetic operations
toolbox.register("evaluate", h)  
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

pop = np.array(toolbox.population(n=POPULATION_SIZE))
