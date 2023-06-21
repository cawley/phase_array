import numpy as np
import dec_SARR
import dec_SIM
import dec_GAv2


def h(arr):
    N = np.shape(arr)[0]

    c1 = np.reshape(np.linspace(0, N - 1, N), (N, 1))
    c2 = np.reshape(np.linspace(0, N - 1, N), (1, N))

    c1 = N - np.abs(c1 - (N - 1) / 2)
    c2 = N - np.abs(c2 - (N - 1) / 2)

    c = c1 + c2

    new_arr = np.cos((arr * (2 * N - 1) - c) * np.pi / c)

    return np.sum(new_arr)

def main():
    N = 16
    population_size = 8
    num_runs = 3000
    arr_ones = np.ones((N, N))
    population = [arr_ones for _ in range(population_size)]

    #out_SARR = dec_SARR.steepestAscentRandomRestart(num_runs, arr_ones)
    out_SIM = dec_SIM.simulatedAnnealing(num_runs, arr_ones)
    out_GA = dec_GAv2.geneticAlgorithm(population, N, population_size)

    return

if __name__ == "__main__":
    main()