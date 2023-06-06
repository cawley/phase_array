import numpy as np
import random as rand
import math
from collections import Counter
from numpy import nonzero
from concurrent.futures import ProcessPoolExecutor

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_lst = list(opt_str)
opt_arr = [i for i in opt_lst if (i == '0' or i == '1')]

inpfile = open("in.txt", "r")
inp_str = inpfile.read()

def generate_random_binary_string(n):
    return list(''.join(rand.choice('01') for _ in range(n)))

state_str = generate_random_binary_string(len(opt_arr))
state = list(state_str)

def generate_bin():
    f = open("in.txt", "w")
    c = 1
    for _ in range(256):
        s = ""
        for _ in range(6):
            r = rand.uniform(0, 1)
            if r > .5:
                s += "1"
            else:
                s += "0"        
        f.write(s)
        f.write(" ")
        c +=1

def fitness(state):
    return sum(s != o for s, o in zip(state, opt_arr))

def roulette_selection(population, scores):
    #population.sort(key = fitness, reverse = True)
    aggregate = 0.0
    for i in range(len(population)):
        aggregate += scores[i]
    prev = 0.0
    p_state = []
    for i in range (len(population)):
        if aggregate != 0:
            p_state.append(prev + (scores[i] / aggregate)) 
        else:
            p_state.append(prev)
        prev = p_state[i]
    r = rand.uniform(0, 1)
    for i in range (len(population)):
        if r < p_state[i]:
            temp = population[i]
            return temp

def breed(p1, p2):
    pivot = rand.randint(1, len(p1) - 2)
    c1 = np.append(p1[:pivot], p2[pivot:])
    c2 = np.append(p2[:pivot], p1[pivot:])
    return [c1, c2]

def random_reset_mutation(c1, r_mut):
    for i in range (len(c1)):
        r = rand.uniform(0, 1)
        if r < r_mut:
            if c1[i] == '1': 
                c1[i] = '0'
            else:
                c1[i] = '1'
    return c1

def split_state(state, n):
    for i in range(0, len(state), n):
        yield state[i:i + n]

def genetic_algorithm(population, r_mut, n_iter):
    convInfo = np.zeros((n_iter, 2))
    idx = 0
    totalItr = 0

    [best, score] = population[0], fitness(population[0])
    h = fitness(population[0])
    for gen in range(n_iter):
        T = gen == 0 and 1 or (1/gen)
        r = rand.uniform(0, 1)

        scores = [fitness(population[i]) for i in range(len(population))]
        totalItr += len(population)
        #check for new best
        for i in range(len(population)):
            if scores[i] < score:
                best, score = population[i], scores[i]
                print(">%d, new best f(%s) = %f" % (gen, population[i], scores[i]))

        if r < T:
            parents = [roulette_selection(population, scores) for _ in range(len(population))]
        else:
            parents = population.copy()
        
        children = list()
        for i in range(0, len(parents) - 1, 2):
            p1, p2 = parents[i], parents[i+1] 
            c1, c2 = breed(p1, p2)
            c1 = random_reset_mutation(c1, r_mut)
            c2 = random_reset_mutation(c2, r_mut)
            children.append(c1)
            children.append(c2)
        population = children.copy()
        for i in range(len(population)):
            if fitness(population[i]) < h:
                h = fitness(population[i])

        convInfo[idx, :] = [totalItr, h]
        idx += 1
        if fitness(population[0]) == 0:
            return [best, score, h], convInfo
    return [best, score, h], convInfo

from functools import partial

def run_ga(r_mut, n_iter, population_part):
    return genetic_algorithm(population_part, r_mut, n_iter)

def main():
    N = 8
    length = len(opt_arr)
    population = [generate_random_binary_string(length) for _ in range(N)] 
    r_mut = .1
    n_iter = 1500

    split_population = list(split_state(population[0], int(len(population[0])/N)))

    with ProcessPoolExecutor() as executor:
        func = partial(run_ga, r_mut, n_iter)
        optimized_arrays = list(executor.map(func, split_population))

    return optimized_arrays

if __name__ == "__main__":
    print(main())