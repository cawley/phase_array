import numpy as np
import random as rand
from matplotlib import pyplot as plt
import math
from collections import Counter
from numpy import nonzero
from functools import partial
import difflib
import time

def split_array(arr):
    s1, s2, s3 = arr.shape[0] // 4, arr.shape[0] // 2, arr.shape[0] * 3 // 4
    p1 = arr[:s1]
    p2 = arr[s1:s2]
    p3 = arr[s2:s3]
    p4 = arr[s3:]
    return p1, p2, p3, p4

start_time = time.time()

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_str = ''.join(opt_str.split())
opt_arr = np.array([i for i in opt_str]).astype(int)
o1, o2, o3, o4 = split_array(opt_arr)

inpfile = open("in.txt", "r")
inp_str = inpfile.read()

def generate_random_binary_string(n):
    copy = opt_arr.copy()
    for i in range(0, len(copy), 10):
        if copy[i] == '1':
            copy[i] = '0'
        else: copy[i] = '1'
    return copy

fitness_dict = {}

def fitness(state, opt):
    return np.sum(abs(state - opt))

def roulette_selection(population, scores):
    populationSize = np.shape(population)[0]
    p_state = scores / np.sum(scores)
    ind = np.random.choice(np.linspace(0, populationSize - 1, populationSize).astype(int), p=p_state, size=(1,), replace=False)
    return population[ind, :]

def breed(p1, p2):
    pivot = rand.randint(1, int(p1.size/2))
    pivot2 = rand.randint(int(p1.size/2), p1.size - 2)
    c1 = np.concatenate((p1[:pivot], p2[pivot:]))
    c2 = np.concatenate((p2[:pivot2], p1[pivot2:]))
    return [c1, c2]

def sextuple_breeding(p1, p2, p3, p4, p5, p6):
    p1 = np.squeeze(p1)
    p2 = np.squeeze(p2)
    p3 = np.squeeze(p3)
    p4 = np.squeeze(p4)
    p5 = np.squeeze(p5)
    p6 = np.squeeze(p6)

    pivot1 = rand.randint(0, int(1 * p1.size/6))
    pivot2 = rand.randint(int(1 * p1.size/6)+1, int(2 * p1.size/6))
    pivot3 = rand.randint(int(2 * p1.size/6)+1, int(3 * p1.size/6))
    pivot4 = rand.randint(int(3 * p1.size/6)+1, int(4 * p1.size/6))
    pivot5 = rand.randint(int(4 * p1.size/6)+1, int(5 * p1.size/6))

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
            inds = np.random.choice(np.linspace(0, c1.size - 1, c1.size).astype(int), size=(2,), replace=False)
            temp = c1[inds[0]]
            c1[inds[0]] = c1[inds[1]]
            c1[inds[1]] = temp
    return c1

def random_reset_mutation(c1, r_mut):
    for i in range (c1.size):
        r = rand.uniform(0, 1)
        if r < r_mut:
            c1[i] = not c1[i]
    return c1

from multiprocessing import Pool

def genetic_algorithm(population, r_mut, n_iter, goal):
    idx = 0
    totalItr = 0

    [best, best_score] = population[0], fitness(population[0], goal)
    h = fitness(population[0], goal)

    # Create a multiprocessing Pool
    pool = Pool()

    partial_fitness = partial(fitness, opt=goal)

    for gen in range(n_iter):
        # Use pool.map() to compute fitness scores in parallel
        scores = pool.map(partial_fitness, population)

        #check for new best
        min_score = np.min(scores)
        min_ind = np.argmin(scores)
        if min_score < best_score:
            best, best_score = population[min_ind], scores[min_ind]
            print(">%d, new best f(%s) = %f" % (gen, best, best_score))

        sorted_population = [x for _, x in sorted(zip(scores, population), key=lambda pair: pair[0])]
        elite_cutoff = int(np.ceil(len(sorted_population) * 1/12)) # This amounts to ~96 elite individuals (1/16)
        elite = sorted_population[:elite_cutoff]
        
        parents = [roulette_selection(population, scores) for _ in range(len(population))]

        children = list()
        r_mut = best_score / np.shape(population)[1]
        for i in range(0, len(parents), 6):
            p1, p2, p3, p4, p5, p6 = parents[i], parents[i+1], parents[i+2], parents[i+3], parents[i+4], parents[i+5]
            c1, c2, c3, c4, c5, c6 = sextuple_breeding(p1, p2, p3, p4, p5, p6)
            c1 = random_reset_mutation(c1, r_mut)
            c2 = random_reset_mutation(c2, r_mut)
            c3 = random_reset_mutation(c3, r_mut)
            c4 = random_reset_mutation(c4, r_mut)
            c5 = random_reset_mutation(c5, r_mut)
            c6 = random_reset_mutation(c6, r_mut)

            children.append(c1)
            children.append(c2)
            children.append(c3)
            children.append(c4)
            children.append(c5)
            children.append(c6)
        population = np.concatenate((children[:-elite_cutoff], elite))

        for i in range(len(population)):
            if fitness(population[i], goal) < h:
                h = fitness(population[i], goal)

        idx += 1
        if fitness(best, goal) == 0:
            pool.close()
            return [best, best_score, h]
    
    pool.close()
    return [best, best_score, h]

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

def split_2d_array(big_array):
    # Calculate the quarter indices
    s1, s2, s3 = big_array.shape[1] // 4, big_array.shape[1] // 2, big_array.shape[1] * 3 // 4

    # Split the array into 4 smaller arrays
    pop1 = big_array[:, :s1]
    pop2 = big_array[:, s1:s2]
    pop3 = big_array[:, s2:s3]
    pop4 = big_array[:, s3:]

    # Return the 4 smaller arrays
    return pop1, pop2, pop3, pop4

def main():
    N = 6
    length = 300
    population = np.random.randint(2, size=(N, length))
    r_mut = .5
    n_iter = 10000

    o1, o2, o3, o4 = split_array(opt_arr)
    o1 = opt_arr[:length]
    pop1 = population

    [b1, s1, h1] = genetic_algorithm(pop1, r_mut, n_iter, o1)
    [b2, s2, h2] = genetic_algorithm(pop2, r_mut, n_iter, o2)
    [b3, s3, h3] = genetic_algorithm(pop3, r_mut, n_iter, o3)
    [b4, s4, h4] = genetic_algorithm(pop4, r_mut, n_iter, o4)
    #[b5, s5, h5] = genetic_algorithm(pop1, r_mut, n_iter)
    #[b6, s6, h6] = genetic_algorithm(pop1, r_mut, n_iter)

    b1_2 = np.concatenate((b1, b2))
    b2_2 = np.concatenate((b3, b4))
    o1_2 = np.concatenate((o1, o2))
    o2_2 = np.concatenate((o3, o4))

    #[b1_2, s1_2, h1_2] = genetic_algorithm(b1_2, r_mut, n_iter, o1_2)
    #[b2_2, s2_2, h3_2] = genetic_algorithm(b2_2, r_mut, n_iter, o2_2)
    #[b3_2, s3_2, h3_2] = genetic_algorithm(np.concatenate((b5, b6)), r_mut, n_iter)

    #[b1_3, s1_3, h1_3] = genetic_algorithm(np.concatenate((b1_2, b2_2)), r_mut, n_iter, opt_arr)
    #[b2_3, s1_3, h1_3] = genetic_algorithm(np.concatenate((b2_2, b2_3)), r_mut, n_iter)

    #[best, score, h] = genetic_algorithm(np.concatenate((b1_3, b2_3)), r_mut, n_iter)

    #[best, score, h] = genetic_algorithm(np.concatenate((b1_3, b2_3)), r_mut, n_iter)
    #print(best)
    #print(score)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The program took {elapsed_time} seconds to run.")


if __name__ == "__main__":
    main()
