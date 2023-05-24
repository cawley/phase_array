import utils
import numpy as np

'''
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
        neighborH = -utils.h(current)
        N = len(current)

        #find best neighbor
        for i in range(N):
            temp = current.copy()

            # move down
            while (temp[i] != 0):
                totalItr += 1
                temp[i] -= 1
                if -utils.h(temp) > neighborH:
                    neighbor = temp.copy()
                    neighborH = -utils.h(temp)

            # move up
            while (temp[i] != N - 1):
                totalItr += 1
                temp[i] += 1
                if -utils.h(temp) > neighborH:
                    neighbor = temp.copy()
                    neighborH = -utils.h(temp)

        if neighborH <= -utils.h(current):
            return current, utils.h(state), utils.h(current), count, convInfo, idx, totalItr, minh
        

        current = neighbor.copy()
        count += 1

        if utils.h(current) < minh:
            minh = utils.h(current)

        convInfo[idx, :] = [totalItr, minh]
        idx += 1


'''
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

    maxConflicts = utils.h(np.zeros((N,)))
    minh = utils.h(state)

    restarts = 0
    steps = 0
    totalItr = 0

    convInfo[idx, :] = [totalItr, minh]
    idx += 1
    totalItr += 1


    for i in range(numRuns):
        # randomize the state
        state = np.random.randint(low=0, high=N, size=(N,))
        for j in range(numRestarts):
            arr, hInitial, currH, count, convInfo, idx, totalItr, minh = steepestAscent(state, convInfo, idx, totalItr, minh)
            steps += count

            # check if the problem is solved
            if currH == 0:
                break
            else:
                # randomize the state
                state = np.random.randint(low=0, high=N, size=(N,))

            restarts += 1
        
        if convInfo[idx - 1, 0] >= maxItr:
            break

    estimateRestarts = restarts / numRuns
    estimateSteps = steps / numRuns

    return estimateRestarts, estimateSteps, convInfo, idx


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
    estimateRestarts, estimateSteps, convInfoFinal, len = steepestAscentRandomRestart(maxItr, state, numRuns=numRuns)
    
    minLen = len
    convInfoFinal = convInfoFinal[:minLen]

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