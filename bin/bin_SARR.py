import utils
import numpy as np

'''
The main steepest ascent algorithm. This function is called after every restart.

input: 
  state: initial state
  convInfo: (2 x n) convergence info
  idx:  current index for convInfo
  totalItr: current number of obj fn calls
  minh: current minimum conflicts

returns:
  current: the final state
  h: the heuristic cost of the final state
  count: the number of steps taken
'''
def steepestAscent(state, convInfo, idx, totalItr, minh):

    current = state.copy()
    count = 0

    while True:
        neighbor = current.copy()
        neighborH = -utils.h2(current)
        N = len(current)

        #find best neighbor
        for i in range(N):
            temp = current.copy()

            # move down
            while (temp[i] != 0):
                totalItr += 1
                temp[i] -= 1
                if -utils.h2(temp) > neighborH:
                    neighbor = temp.copy()
                    neighborH = -utils.h2(temp)

            # move up
            while (temp[i] != 2 - 1):
                totalItr += 1
                temp[i] += 1
                if -utils.h2(temp) > neighborH:
                    neighbor = temp.copy()
                    neighborH = -utils.h2(temp)

        if neighborH <= -utils.h2(current):
            return current, utils.h2(state), utils.h2(current), count, convInfo, idx, totalItr, minh
        

        current = neighbor.copy()
        count += 1

        if utils.h2(current) < minh:
            minh = utils.h2(current)
            print('Run: {}, h: {}'.format(totalItr, minh))

        convInfo[idx, :] = [totalItr, minh]
        idx += 1


'''
Function implementing random restarts

input:
  maxItr: max number of obj fn calls
  state: initial state
  runRuns: number of runs
  rumRestarts: number of restarts

returns:
  estimateRestarts: Empirical estimate of the expected number of restarts
  estimateSteps: Empirical estimate of the expected total number of steps across restarts
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls

'''
def steepestAscentRandomRestart(maxItr, state, numRuns=1000, numRestarts=100):

    convInfo = np.zeros((10000, 2))
    idx = 0

    N = len(state)

    maxConflicts = utils.h2(np.zeros((N,)))
    minh = utils.h2(state)

    restarts = 0
    steps = 0
    totalItr = 0

    convInfo[idx, :] = [totalItr, minh]
    idx += 1
    totalItr += 1

    for i in range(numRuns):
        # randomize the state
        state = np.random.randint(low=0, high=2, size=(N,))
        for j in range(numRestarts):
            arr, hInitial, currH, count, convInfo, idx, totalItr, minh = steepestAscent(state, convInfo, idx, totalItr, minh)
            steps += count

            # check if the problem is solved
            if currH == 0:
                break
            else:
                # randomize the state
                state = np.random.randint(low=0, high=2, size=(N,))

            restarts += 1
        
        if convInfo[idx - 1, 0] >= maxItr:
            break

    estimateRestarts = restarts / numRuns
    estimateSteps = steps / numRuns

    return estimateRestarts, estimateSteps, convInfo, idx


'''
Average results from numLoops runs of the algorithm

input:
  numLoops: number of loops to average over
  state: initial state
  runRuns: number of runs per loop
  rumRestarts: number of restarts

returns:
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls, averaged over numLoops calls

'''
def repeatSARR(maxItr, numLoops, state, numRuns, numRestarts):
    estimateRestarts, estimateSteps, convInfoFinal, len = steepestAscentRandomRestart(maxItr, state, numRuns=numRuns)
    
    minLen = len
    convInfoFinal = convInfoFinal[:minLen]
    print("Repeat SARR")
    for i in range(numLoops - 1):
        estimateRestarts, estimateSteps, convInfo, len = steepestAscentRandomRestart(maxItr, state, numRuns=100)

        if len < minLen:
            minLen = len
        
        convInfo = convInfo[:minLen]
        convInfoFinal = convInfoFinal[:minLen]

        convInfoFinal += convInfo
        print(i)
    
    convInfoFinal /= numLoops

    return convInfoFinal