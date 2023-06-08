import numpy as np
import random as rand
from matplotlib import pyplot as plt
import math
from collections import Counter
from numpy import nonzero
import time

start_time = time.time()

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_arr = np.array([i for i in opt_str if (i == '0' or i == '1')])

inpfile = open("in.txt", "r")
inp_str = inpfile.read()

def generate_random_binary_string(n):
    return np.array([rand.choice('01') for _ in range(n)])

fitness_dict = {}

def fitness(state):
    state_string = ''.join(state)
    # Check if fitness for this state is already computed
    if state_string in fitness_dict:
        return fitness_dict[state_string]
    else:
        fit_score = np.sum(state != opt_arr)
        fitness_dict[state_string] = fit_score
        return fit_score

def roulette_selection(population, scores):
    aggregate = np.sum(scores)
    p_state = np.cumsum(scores) / aggregate
    r = rand.uniform(0, 1)
    for i in range(len(population)):
        if r <= p_state[i]:
            return population[i]
    return population[-1]

def breed(p1, p2):
    pivot = rand.randint(1, int(p1.size/2))
    pivot2 = rand.randint(int(p1.size/2), p1.size - 2)
    c1 = np.concatenate((p1[:pivot], p2[pivot:]))
    c2 = np.concatenate((p2[:pivot2], p1[pivot2:]))
    return [c1, c2]

def sextuple_breeding(p1, p2, p3, p4, p5, p6):
    pivot1 = rand.randint(1, int(1 * p1.size/6))
    pivot2 = rand.randint(int(1 * p1.size/6), int(2 * p1.size/6))
    pivot3 = rand.randint(int(2 * p1.size/6), int(3 * p1.size/6))
    pivot4 = rand.randint(int(3 * p1.size/6), int(4 * p1.size/6))
    pivot5 = rand.randint(int(4 * p1.size/6), int(5 * p1.size/6))

    c1 = np.concatenate((p1[:pivot1], p2[pivot1:pivot2], p3[pivot2:pivot3], p4[pivot3:pivot4], p5[pivot4:pivot5], p6[pivot5:]))
    c2 = np.concatenate((p2[:pivot1], p3[pivot1:pivot2], p4[pivot2:pivot3], p5[pivot3:pivot4], p6[pivot4:pivot5], p1[pivot5:]))
    c3 = np.concatenate((p3[:pivot1], p4[pivot1:pivot2], p5[pivot2:pivot3], p6[pivot3:pivot4], p1[pivot4:pivot5], p2[pivot5:]))
    c4 = np.concatenate((p4[:pivot1], p5[pivot1:pivot2], p6[pivot2:pivot3], p1[pivot3:pivot4], p2[pivot4:pivot5], p3[pivot5:]))
    c5 = np.concatenate((p5[:pivot1], p6[pivot1:pivot2], p1[pivot2:pivot3], p2[pivot3:pivot4], p3[pivot4:pivot5], p4[pivot5:]))
    c6 = np.concatenate((p6[:pivot1], p1[pivot1:pivot2], p2[pivot2:pivot3], p3[pivot3:pivot4], p4[pivot4:pivot5], p5[pivot5:]))

    return [c1, c2, c3, c4, c5, c6]

def swapmutation(c1, r_mut):
    r = rand.uniform(0, 1)
    for _ in range(c1.size):
        if r < r_mut:
            rpos1, rpos2 = rand.randint(0, c1.size - 1), rand.randint(0, c1.size - 1)
            c1[rpos1], c1[rpos2] = c1[rpos2], c1[rpos1]
    return c1

def random_reset_mutation(c1, r_mut):
    for i in range (c1.size):
        r = rand.uniform(0, 1)
        if r < r_mut:
            c1[i] = '1' if c1[i] == '0' else '0'
    return c1

from multiprocessing import Pool

def genetic_algorithm(population, r_mut, n_iter):
    idx = 0
    totalItr = 0

    [best, score] = population[0], fitness(population[0])
    h = fitness(population[0])

    # Create a multiprocessing Pool
    pool = Pool()

    for gen in range(n_iter):
        # Use pool.map() to compute fitness scores in parallel
        scores = pool.map(fitness, population)

        #check for new best
        for i in range(len(population)):
            if scores[i] < score:
                best, score = population[i], scores[i]
                print(">%d, new best f(%s) = %f" % (gen, population[i], scores[i]))

        sorted_population = [x for _, x in sorted(zip(scores, population), key=lambda pair: pair[0])]
        elite_cutoff = int(len(sorted_population) * 0.0625) # This amounts to ~96 elite individuals (1/16)
        elite = sorted_population[:elite_cutoff]
        
        parents = [roulette_selection(population, scores) for _ in range(len(population))]

        children = list()
        for i in range(0, len(parents) - 1, 6):
            p1, p2, p3, p4, p5, p6 = parents[i], parents[i+1], parents[i+2], parents[i+3], parents[i+4], parents[i+5]
            c1, c2, c3, c4, c5, c6 = sextuple_breeding(p1, p2, p3, p4, p5, p6)
            c1 = swapmutation(c1, r_mut)
            c2 = random_reset_mutation(c2, r_mut)
            c3 = swapmutation(c3, r_mut)
            c4 = random_reset_mutation(c4, r_mut)
            c5 = swapmutation(c5, r_mut)
            c6 = random_reset_mutation(c6, r_mut)
            children.append(c1)
            children.append(c2)
            children.append(c3)
            children.append(c4)
            children.append(c5)
            children.append(c6)
        population = children[:len(children) - elite_cutoff] + elite

        for i in range(len(population)):
            if fitness(population[i]) < h:
                h = fitness(population[i])

        idx += 1
        if fitness(best) == 0:
            pool.close()
            return [best, score, h]
    
    pool.close()
    return [best, score, h]

from joblib import Parallel, delayed

def worker(args):
    return genetic_algorithm(*args)

def parallel_genetic_algorithms(population, r_mut, n_iter):
    s1, s2, s3, s4, s5 = int(population.size/6), int(2 * population.size/6), int(3 * population.size/6), int(4 * population.size/6), int(5 * population.size/6)
    pop1 = population[:s1]
    pop2 = population[s1:s2]
    pop3 = population[s2:s3]
    pop4 = population[s3:s4]
    pop5 = population[s4:s5]
    pop6 = population[s5:]

    pops = [pop1, pop2, pop3, pop4, pop5, pop6]
    args = [(pop, r_mut, n_iter) for pop in pops]

    results = Parallel(n_jobs=-1)(delayed(worker)(arg) for arg in args)

    # results is now a list of tuples [(b1, s1, h1), (b2, s2, h2), ..., (b6, s6, h6)]
    # if you want separate lists for b, s, and h values, you can do the following:
    b_values, s_values, h_values = zip(*results)

    return b_values, s_values, h_values

def main():
    N = 150
    length = 1536
    population = np.array([generate_random_binary_string(length) for _ in range(N)])
    r_mut = .2
    n_iter = 1000

    print(fitness(population[0]))
    
    s1, s2, s3, s4, s5 = int(population.size/6), int(2 * population.size/6), int(3 * population.size/6), int(4 * population.size/6), int(5 * population.size/6)
    pop1 = population[:s1]
    pop2 = population[s1:s2]
    pop3 = population[s2:s3]
    pop4 = population[s3:s4]
    pop5 = population[s4:s5]
    pop6 = population[s5:]

    pops = [pop1, pop2, pop3, pop4, pop5, pop6]
    
    [b1, s1, h1] = genetic_algorithm(pop1, r_mut, n_iter)
    [b2, s2, h2] = genetic_algorithm(pop1, r_mut, n_iter)
    [b3, s3, h3] = genetic_algorithm(pop1, r_mut, n_iter)
    [b4, s4, h4] = genetic_algorithm(pop1, r_mut, n_iter)
    [b5, s5, h5] = genetic_algorithm(pop1, r_mut, n_iter)
    [b6, s6, h6] = genetic_algorithm(pop1, r_mut, n_iter)

    [b1_2, s1_2, h1_2] = genetic_algorithm(np.concatenate((b1, b2)), r_mut, n_iter)
    [b2_2, s2_2, h3_2] = genetic_algorithm(np.concatenate((b3, b4)), r_mut, n_iter)
    [b3_2, s3_2, h3_2] = genetic_algorithm(np.concatenate((b5, b6)), r_mut, n_iter)

    [b1_3, s1_3, h1_3] = genetic_algorithm(np.concatenate((b1_2, b2_2)), r_mut, n_iter)
    [b2_3, s1_3, h1_3] = genetic_algorithm(np.concatenate((b2_2, b2_3)), r_mut, n_iter)

    [best, score, h] = genetic_algorithm(np.concatenate((b1_3, b2_3)), r_mut, n_iter)

    print(best)
    print(score)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The program took {elapsed_time} seconds to run.")


if __name__ == "__main__":
    main()
