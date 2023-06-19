import numpy as np
import random as rand
from matplotlib import pyplot as plt
import math
from collections import Counter
from numpy import nonzero
import time

start_time = time.time()

global n_sub
n_sub = 1536

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_arr = np.array([i for i in opt_str if (i == '0' or i == '1')])

opt_arr_copy = opt_arr[:n_sub]
opt_arr = opt_arr_copy
opt_int = [int(i) for i in opt_arr_copy]
opt_int = np.zeros(n_sub)

inpfile = open("in.txt", "r")
inp_str = inpfile.read()

def generate_random_binary_string(n):
    return np.array([rand.choice('01') for _ in range(n)])

def generate_random_bin_array(n):
    return np.zeros(n)

# Fitness dictionary to store previously computed fitness scores
fitness_dict = {}

def encoding(state):
    arr = np.resize(arr, (len(arr) // 6, 6))
    
    # Convert binary to decimal using NumPy's binary_repr function
    decimals = np.array([int(''.join(row), 2) for row in arr])
    
    return decimals


def fitness(state):
    a = tuple(state)
    # Check if fitness for this state is already computed
    if a in fitness_dict:
        return fitness_dict[a]
    else:
        fit_score = np.sum(state)
        fitness_dict[a] = fit_score
        return fit_score

global gbest
global gbest_score

def pso(n_sub, n_parts, n_iter):
    convInfo = np.zeros((n_iter, 2))
    gbest = [63]*n_sub 
    gbest_score = np.inf

    cognitive = 1
    social = 1
    inertia = 1
    r_maxv = 4

    particles = [{'states': [rand.randint(0, 63) for _ in range(n_sub // 6)],
                  'pbest': [1]*n_sub,
                  'pbest_score': n_sub,
                  'v': [rand.randint(0, r_maxv) for _ in range(n_sub // 6)]} for _ in range(n_parts)]
                  
    h = fitness(particles[0]['states'])

    for i in range(n_iter):
        for particle in particles:
            score = fitness(particle['states'])
            particle['score'] = score
            if score < particle['pbest_score']:
                particle['pbest'] = particle['states'].copy()
                particle['pbest_score'] = score

            if score < gbest_score:
                gbest = particle['states'].copy()
                gbest_score = score
                print(f"> {i}: New Global Best: {gbest} Score: {gbest_score}\n")

            for particle_idx, particle in enumerate(particles):
                for state_idx, state_val in enumerate(particle['states']):
                    r = rand.randint(0, 2)
                    particle['states'][state_idx] = inertia * particle['v'][state_idx] + cognitive * r * (particle['pbest'][state_idx] - state_val) + social * r * (gbest[state_idx] - state_val)
                    particle['states'][state_idx] = (particle['states'][state_idx] + particle['v'][state_idx]) % (64)
        
        for j in range(len(particles)):
            if fitness(particles[j]['states']) < h:
                h = fitness(particles[j]['states'])

        convInfo[i, :] = [i, h]

    return gbest, h, convInfo

def repeatPSO(maxItr, numLoops, initState, numRuns):
    # N SUB IS THE LENGTH OF THE STRING
    # N PARTS IS THE POPULATION SIZE
    n_iter = maxItr
    n_sub = 8
    n_parts = 8
    gbest, h, convInfoFinal = pso(n_sub, n_parts, n_iter)
    
    print("Repeat PSO")
    for i in range(numLoops - 1):
        best, hv, convInfo = pso(n_sub, n_parts, n_iter)
        convInfoFinal += convInfo
        print(i)
    
    convInfoFinal /= numLoops
    return convInfoFinal

def main():
    '''
    n_sub = int(input("N (Queens)")) 
    n_parts = int(input("Swarm Quantity"))
    n_iter = int(input("Iteration Count"))
    n_samp = int(input("Amount of Trials"))

    '''
    n_parts = 12
    n_iter = 10000
    n_samp = 10

    g, s, c = pso(n_sub, n_parts, n_iter)

    print(g, s)

    '''
    totalh = 0
    for i in range(n_samp):
        g, h, conv = pso(n_sub, n_parts, n_iter)
        totalh += h
    print(f"H Score: {totalh/n_samp}")
    '''

if __name__ == "__main__":
    main()
