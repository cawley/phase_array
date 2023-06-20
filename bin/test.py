import numpy as np
import random as rand
from matplotlib import pyplot as plt
import math
from collections import Counter
from numpy import nonzero
from functools import partial
import difflib
import time
import bin_splitGA_sextuplet_breeding
import bin_SARR
import bin_SIM

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_str = ''.join(opt_str.split())
opt_arr = np.array([i for i in opt_str]).astype(int)

M = int(np.shape(opt_arr)[0])
pivot = M // 4
o1, o2, o3, o4 = opt_arr[0:pivot], opt_arr[pivot:2*pivot], opt_arr[2*pivot:3*pivot], opt_arr[3*pivot:]


def main():
    N = 6
    length = 300
    population = np.random.randint(2, size=(N, length))
    r_mut = .5
    n_iter = 10000

    o1 = opt_arr[:length]
    pop1 = population


    out_SARR = bin_SARR.steepestAscentRandomRestart(n_iter, np.squeeze(population[0, :]))
    out_GA = bin_splitGA_sextuplet_breeding.genetic_algorithm(pop1, r_mut, n_iter, o1)
    out_SIM = bin_SIM.simulatedAnnealing(n_iter, np.squeeze(population[0, :]))

    return


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
