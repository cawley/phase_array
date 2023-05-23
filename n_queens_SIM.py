import utils
import numpy as np

'''
input:
  maxItr: max number of obj fn calls
  state: initial state
  runRuns: number of runs

returns:
  estimateRestarts: Empirical estimate of the expected number of restarts
  estimateSteps: Empirical estimate of the expected total number of steps across restarts
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls

'''
def simulatedAnnealing(maxItr, state, numRuns=1000, numRestarts=100):
    convInfo = np.zeros((10000, 2))
    idx = 0

    N = len(state)

    for i in range(numRuns):
      np.random.randint(low=0, high=N)
    
    return convInfo

      


'''
input:
  numLoops: number of loops to average over
  state: initial state
  runRuns: number of runs per loop
  rumRestarts: number of restarts

returns:
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls, averaged over numLoops calls

'''
def repeatSARR(maxItr, numLoops, state, numRuns, numRestarts):
    convInfoFinal = simulatedAnnealing(maxItr, state, numRuns=numRuns)

    for i in range(numLoops - 1):
        estimateRestarts, estimateSteps, convInfo, len = simulatedAnnealing(maxItr, state, numRuns=100)
        convInfoFinal += convInfo
        print(i)
    
    convInfoFinal /= numLoops

    return convInfoFinal