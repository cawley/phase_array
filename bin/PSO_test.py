import numpy as np
import random as rand

n_sub, n_parts, n_iter, r_maxv = 15, 4, 100, 3

particles = [{'states': [rand.randint(0, 1) for _ in range(n_sub)],
                  'pbest': [-1]*n_sub,
                  'pbest_score': n_sub,
                  'v': [rand.randint(0, r_maxv) for _ in range(n_sub)]} for _ in range(n_sub)]

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_arr = np.array([i for i in opt_str if (i == '0' or i == '1')])

opt_arr_copy = opt_arr[:n_sub]
opt_arr = opt_arr_copy
opt_int = [int(i) for i in opt_arr_copy]
print(opt_int)

fitness_dict = {}
def fitness(state):
    a = tuple(state)
    # Check if fitness for this state is already computed
    if a in fitness_dict:
        return fitness_dict[a]
    else:
        fit_score = np.sum(state != opt_int)
        fitness_dict[a] = fit_score
        return fit_score

def f(state):
    return np.sum(state != opt_int)

def generate_random_bin_array(opt_int):
    opt_int_copy = opt_int.copy()
    for i in range(len(opt_int_copy)):
        if opt_int[i] == 1: 
            opt_int_copy[i] = 0
        else: 
            opt_int_copy[i] = 1
    print(opt_int_copy)
    return opt_int_copy

print(opt_int)
print(f(generate_random_bin_array(opt_int)))

