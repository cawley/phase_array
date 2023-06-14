import numpy as np
import random as rand

n_sub, n_parts, n_iter, r_maxv = 15, 4, 100, 3

particles = [{'states': [rand.randint(0, 1) for _ in range(n_sub)],
                  'pbest': [-1]*n_sub,
                  'pbest_score': n_sub,
                  'v': [rand.randint(0, r_maxv) for _ in range(n_sub)]} for _ in range(n_sub)]

opt_int = np.zeros(n_sub)

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
    return np.sum(state)

def max_diff(opt_int):
    opt_int_copy = opt_int.copy()
    for i in range(len(opt_int_copy)):
        opt_int_copy[i] = opt_int[i] ^ opt_int[i]
    print(opt_int_copy)
    return opt_int_copy

def generate_random_bin_array(n):
    a = np.array([])
    for i in range(n):
        r = rand.uniform(0, 1)
        if r < .5:
            a.append(1)
        else:
            a.append(0)
print(opt_int)
print(f(generate_random_bin_array(len(opt_int))))

