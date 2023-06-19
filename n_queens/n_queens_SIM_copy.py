import utils
import numpy as np
import copy

'''
input:
  maxItr: max number of obj fn calls
  state: initial state
  runRuns: number of runs

returns:
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls

'''
def simulatedAnnealing(maxItr, state, num_runs=1000, tunneling_prob=0):
  total_itr = 0
  convInfo = np.zeros((maxItr, 2))

  N = len(state)
  maxConflicts = utils.h2(np.zeros((N,)))
  minh = maxConflicts
  currh = utils.h2(state)

  for i in range(maxItr):
    T = (1 - (i + 1)/maxItr)

    # with probability tunnelingProb, generate next state very far away from current
    if np.random.uniform(low=0, high=1) < tunneling_prob:
      next = state.copy()
      numRand = int(np.ceil(T*N))
      inds = np.random.choice(np.linspace(0, N - 1, N).astype(int), size=(numRand,), replace=False)
      for ind in inds:
        val = np.random.randint(low=0, high=2)
        next[ind] = val
        
    else:
      ind = np.random.randint(low=0, high=N)
      val = np.random.randint(low=0, high=2)
      next = state.copy()
      next[ind] = val

    nexth = utils.h2(next)
    total_itr += 1


    deltaE = currh - nexth
    if T != 0:
      P = 1 / (1 + np.exp(-deltaE / T))
    else:
      P = 0

    if deltaE > 0:
      state = next.copy()
      currh = nexth
    elif np.random.uniform(low=0, high=1) < P:
      state = next.copy()
      currh = nexth
            
    if currh < minh:
       minh = currh 
       print('Run: {}, h: {}'.format(total_itr, minh))
       if minh == 0:
         return

    convInfo[i, :] = [i, minh]

      
  return convInfo

'''
input:
  maxItr: max number of obj fn calls
  numLoops: number of loops to average over
  state: initial state
  runRuns: number of runs per loop

returns:
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls, averaged over numLoops calls
'''
def repeatSIM(maxItr, numLoops, state, numRuns, tunnelingProb=0):
    numRuns = maxItr
    convInfoFinal = simulatedAnnealing(maxItr, state, numRuns, tunnelingProb)
    print("Repeat SIM")
    for i in range(numLoops - 1):
        convInfo = simulatedAnnealing(maxItr, state, numRuns, tunnelingProb)
        convInfoFinal += convInfo
        print(i)
    
    convInfoFinal /= numLoops

    return convInfoFinal