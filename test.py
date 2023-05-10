import utils as utils
import numpy as np
import tensorflow as tf
import math as m
import random as rand

'''
GENETIC ALGORITHM TEST
'''

def one_to_two(pop):
    mat = [x[:] for x in [[0] * len(pop)] * len(pop)]
    for i in range(len(pop)):
        mat[i][pop[i]] = 1
    return mat

def two_to_one(mat):
    pop = [0 for i in range(len(mat[0]))]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 1:
                pop[i] = j

def objective(pop):
    return utils.h(pop)

#tournament selection
def selection(pop, scores, k = 3):
    #first random selection
    selection_i = rand.randint(len(pop))
    for i in rand.randint(0, len(pop), k-1):
        if scores[i] < scores[selection_i]:
            selection_i = i;
            
    return pop[selection_i]

#create next generation after crossover

#let crossover crossbreed two parents to create two children
def crossover(p1, p2, r_cross):
    #initialize children to be copies of parents
    c1, c2 = p1.copy(), p2.copy()
    #check for recombination
    if rand() < r_cross:
        pivot = rand.randint(1, len(p1) - 2)
        c1 = p1[:pivot] + p2[:pivot]
        c2 = p2[:pivot] + p1[:pivot]
    return [c1, c2]

#mutate a child
def mutation(child, r_mut):
    for i in range(len(child)):
        #check for a mutation
        if rand() < r_mut:
            child[i] = rand.randint(0, 7) 

#hyperparameters
n_pop = 4 #population size
n_bits = 8 #single candidate solution size
n_iter = 100 #algorithm iterations
r_cross = 0.85 #crossbreeding rate
r_mut = 0.15 #mutuation rate

def genetic_algorithm(pop, objective, n_bits, n_iter, n_pop, r_cross, r_mut):
    
    mat = one_to_two(pop)
    best, best_eval = 0, objective(mat[0])

    for gen in range(n_iter):
        scores = [objective(c) for c in pop]

        #check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))

        #select parents
        parents = [selection(pop, scores) for _ in range(n_pop)]

        #create next generation
        children = list()
        for i in range(0, n_pop, 2):
            #select parents in pairs
            p1, p2 = parents[i], parents[i+1]
            for c in crossover(p1, p2, r_cross):
                mutation(c, r_mut)
                children.append(c)
        pop = children
    return [best, best_eval]



