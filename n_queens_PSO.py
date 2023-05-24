import math as math
import random as rand
import numpy as np

out = open('out.txt', 'w') 

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
    # X || V meaning they are identically indexed and make up the same population of particles
    x = [[(rand.randint(0, n_sub - 1)) for _ in range(n_sub)] for _ in range(n_parts)]
    xprev = x.copy()
    v = [[(rand.randint(0, r_maxv)) for _ in range(n_sub)] for _ in range(n_parts)]

    # global inits
    best = x[0]
    best_score = fitness(best)
    gbest = best
    gbest_score = fitness(gbest)
    # local best inits
    pbest = [[0] * n_sub for _ in range(n_parts)]
    scores = []

    c = 0
    print("\n")
    while (best_score < max_conflicts(x[0])) and (c < n_iter):
        # calculate scores to compare
        print("Iteration:", c)

        for i in range(n_parts):
            for j in range(len(v[i])):
                r = rand.randint(0, 2)
                v[i][j] = inertia * v[i][j] + cognitive * r * (pbest[i][j] - x[i][j]) + social * r * (x[pbest.index(max(pbest))][j] - x[i][j])
                # v[i][j] is the velocity of particle i in dimension j, 
                # x[i][j] is the current position of particle i in dimension j, 
                # pbest[i][j] is the personal best position of particle i in dimension j, 
                # gbest[j] is the global best position in dimension j, 
                # w is the inertia weight, c1 and c2 are cognitive and social coefficients, respectively,
                # rand() is a random number between 0 and 1.
                x[i][j] += v[i][j]
                x[i][j] = x[i][j] % n_sub
        
        scores = [fitness(x[i]) for i in range(n_parts)]
        pbest_scores = [fitness(pbest[i]) for i in range(n_parts)]
        
        # update current best
        best = x[scores.index(max(scores))]
        best_score = max(scores)

        # update pbest list (highest score across a certain index)
        pbest[:] = [x[i] for i in range(len(pbest)) if fitness(pbest[i]) <= fitness(x[i])]

        # update global best (best of the pbest)
        if best_score > max(pbest_scores): 
            gbest = best 
            gbest_score = best_score
        else:
            gbest = pbest[pbest_scores.index(max(pbest_scores))]
            gbest_score = fitness(pbest[pbest_scores.index(max(pbest_scores))])     
        print("X:")
        for i in range(len(x)):
            print(x[i], scores[i], pbest[i], fitness(pbest[i]))
        print("PBEST Max:", pbest[pbest_scores.index(max(pbest_scores))]) 
        print("Scores Max:", max(scores), "Max Score IDX", scores.index(max(scores)))
        print("Best State:", best, "Best Score:", best_score)
        print("Global Best:", gbest, fitness(gbest),"\n")
        c+=1
    print("\n", "GLOBALS: STATE =", gbest, "SCORE =", gbest_score, "\n")
    return gbest
    

def main():
    #HYPERPARAMS
    cognitive = 1 #C1
    social = 1    #C2
    inertia = 1   #W

    #MAKE PARTICLES, SUB PARTICLE RANGE (0, N_SUB)
    n_sub = 4   #BOARD SIZE (N in NQUEEN)
    n_parts = 4 #POPULATION SIZE 
    r_maxv = 3
    n_iter = 10

    g = pso(n_sub, n_parts, r_maxv, n_iter, cognitive, social, inertia)

    print(max_conflicts(g))
    print(fitness(g))

if __name__ == "__main__":
    main()

