import math as math
import random as rand
import numpy as np

def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    
    return (row1 == row2 or                 # same row
            col1 == col2 or                 # same column 
            row1 - col1 == row2 - col2 or   # same \ diagonal
            row1 + col1 == row2 + col2)     # same / diagonal

def conflicts(state):
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1 + 1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return num_conflicts

def max_conflicts(state):
    temp = state.copy()
    for i in range(len(temp)):
        temp[i] = 0
    return conflicts(temp)

def fitness(state_in):
    state = state_in.copy()
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1 + 1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return (max_conflicts(state) - num_conflicts)

def pso(n_sub, n_parts, r_maxv, n_iter, cognitive, social, inertia):
    #X || V meaning they are identically indexed and make up the same population of particles
    x = np.random.rand(n_sub, n_parts) * n_sub    #ELEM ~U(0, n_sub)
    v = np.random.randn(n_sub, n_parts) * r_maxv  #ELEM ~N(0, r_maxv)

    best = x[0]
    best_score = fitness(best)
    best_idx = 0

    pbest = [0] * n_parts
    scores = []

    i = 0
    while (best_score != max_conflicts(x[0])) and (i < n_iter):
        scores = [fitness(x[i]) for i in range(n_parts)]
        for i in range(len(scores)):
            if scores[i] > pbest[i]:
                pbest[i] = scores[i]
        gbest = max(pbest)
        gbest_idx = index(gbest)
        for i in range(len(scores)):
            for j in range(len(v[i])):
                v[i][j] = inertia * v[i][j] + cognitive * rand() * (pbest[i] - x[i][j]) + social * rand() * (x[gbest_idx] - x[i][j])
                # Here, v[i][j] is the velocity of particle i in dimension j, 
                # x[i][j] is the current position of particle i in dimension j, 
                # pbest[i] is the personal best position of particle i in dimension j, 
                # gbest[j] is the global best position in dimension j, 
                # w is the inertia weight, c1 and c2 are cognitive and social coefficients, respectively,
                # rand() is a random number between 0 and 1.
                x[i][j] += v[i][j]
        best = x[gbest_idx]
    return best

def main():
    #HYPERPARAMS
    cognitive = 1 #C1
    social = 1    #C2
    inertia = 2   #W

    #MAKE PARTICLES, SUB PARTICLE RANGE (0, N_SUB)
    n_sub = 8   #BOARD SIZE (N in NQUEEN)
    n_parts = 4 #POPULATION SIZE 
    r_maxv = 0.25
    n_iter = 100

    print(pso(n_sub, n_parts, r_maxv, n_iter, cognitive, social, inertia))

if __name__ == "__main__":
    main()

