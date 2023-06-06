import numpy as np
import random as rand
from matplotlib import pyplot as plt
import math
from collections import Counter
from numpy import nonzero

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

'''
# This fitness function is defined as the cosine between the angles that these two vectors create
def fitness(state):
    # state as compared to opt_arr 
    c1 = Counter(state)
    c2 = Counter(opt_arr)
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magSt = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magOp = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magSt * magOp)
'''

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

# SINGLE POINT CROSSOVER BREEDING
# https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
def breed(p1, p2):
    pivot1 = rand.randint(1, int(len(p1)/2) - 2)
    pivot2 = rand.randint(int(len(p1)/2), int(len(p1)) - 2)
    c1 = np.append(p1[:pivot1], p2[pivot1:])
    c2 = np.append(p2[:pivot2], p1[pivot2:])
    return [c1, c2]

# SWAP MUTATION GA
# https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)
def swapmutation(c1, r_mut):
    r = rand.uniform(0, 1)
    for _ in range(len(c1[0])):
        if r < r_mut:
            rpos1, rpos2 = rand.randint(0, len(c1[0])), rand.randint(0, len(c1[0]))
            temp = c1[0][rpos1]
            c1[0][rpos1] = c1[0][rpos2]
            c1[0][rpos2] = temp
    return c1

# RANDOM RESET MUTATION
# https://www.geeksforgeeks.org/mutation-algorithms-for-string-manipulation-ga/
def random_reset_mutation(c1, r_mut):
    for i in range (len(c1)):
        r = rand.uniform(0, 1)
        if r < r_mut:
            if c1[i] == '1': 
                c1[i] = '0'
            else:
                c1[i] = '1'
    return c1

# STANDARD GA FOR N QUEENS WITH ALL PARAMS MENTIONED  
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
        if fitness(best) == 0:
            return [best, score, h], convInfo
    return [best, score, h], convInfo

def main():
    N = 16
    length = len(opt_arr)
    population = [generate_random_binary_string(length) for _ in range(N)] 
    r_mut = .001
    n_iter = 15000
    print(fitness(population[0]))
    [best, score, h], convInfo = genetic_algorithm(population, r_mut, n_iter)
    print(best)
    print(score)


if __name__ == "__main__":
    main()