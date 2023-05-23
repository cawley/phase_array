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
  numLoops = 30

  convInfoSARR = n_queens_SARR.repeatSARR(maxItr, numLoops, initialState, 100, 100)

  _, convInfoGAv2 = n_queens_GAv2.geneticAlgorithm(population=[initialState.copy() for _ in range(4)], N=N, populationSize=4, numRuns=4000)

  plt.plot(convInfoSARR[:, 0], convInfoSARR[:, 1], label='Steepest Ascent with Random Restart')
  plt.plot(convInfoGAv2[:, 0], convInfoGAv2[:, 1], label='Genetic Algorithm')
  plt.show()


  return

if __name__ == "__main__":
    main()