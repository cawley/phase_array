import copy
import random
import math
import random
import numpy as np

def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    return (row1 == row2 or  # same row
            col1 == col2 or  # same column
            row1 - col1 == row2 - col2 or  # same \ diagonal
            row1 + col1 == row2 + col2)  # same / diagonal

def h(state):
    """Return number of conflicting queens for a given node.
    state: a list of length 'n' for n-queens problem,
    where the c-th element of the list holds the value for the row number of the queen in column c.
    """
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1+1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return num_conflicts

def h2(state):
    return np.sum(abs(state - np.ones(np.shape(state))))

# 5.3
'''
input:
    N: number of queens
    populationSize: size of the population
    mutationRate: rate of mutation
    numRuns: number of runs

returns:
    minh: minimum h value over all (populationSize * runRuns) states
    
    Gabe Ronan
'''
def geneticAlgorithm(N=8, populationSize=4, mutationRate=0.15, numRuns=100):
    exampleState = np.random.randint(low=0, high=N, size=(N,))
    exampleNumConflicts = h(exampleState)
    minh = exampleNumConflicts
	
    return minh