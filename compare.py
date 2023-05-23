import numpy as np
import n_queens_SARR
import n_queens_GA
import n_queens_GAv2
import n_queens_PSO
import matplotlib.pyplot as plt

def main():
    N = 8
    initialState = np.random.randint(low=0, high=N, size=(N,))
    maxItr = 10000
    numLoops = 40

    convInfoSARR = n_queens_SARR.repeatSARR(maxItr, numLoops, initialState, 100, 100)

    popSize = 4
    convInfoGA = n_queens_GA.repeatGA(maxItr, numLoops, population=[initialState.copy() for _ in range(popSize)], numRuns=4000)
    convInfoGAv2 = n_queens_GAv2.repeatGAv2(maxItr, numLoops, population=[initialState.copy() for _ in range(popSize)], N=N, populationSize=popSize, numRuns=4000)

    line1, = plt.plot(convInfoSARR[:, 0], convInfoSARR[:, 1], label='Steepest Ascent with Random Restart')
    line2, = plt.plot(convInfoGA[:, 0], convInfoGA[:, 1], label='Genetic Algorithm')
    line3, = plt.plot(convInfoGAv2[:, 0], convInfoGAv2[:, 1], label='Genetic Algorithm V2')
    plt.legend(handles=[line1, line2, line3])

    plt.show()

    return

if __name__ == "__main__":
    main()