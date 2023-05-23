import utils
import numpy as np

'''
input: 
  stateinitial state

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

# 5.2
'''
input: 
  state: initial state
  runRuns: number of runs
  rumRestarts: number of restarts

returns:
  estimateRestarts: Empirical estimate of the expected number of restarts
  estimateSteps: Empirical estimate of the expected total number of steps across restarts
  convInfo: (2 x n) matrix of minimum conflicts and number of objective function calls

'''
def steepestAscentRandomRestart(state, numRuns=1000, numRestarts=100):

    convInfo = np.zeros((1000, 2))
    idx = 0

    N = len(state)

    maxConflicts = utils.h(np.zeros((N,)))
    minh = maxConflicts

    restarts = 0
    steps = 0
    totalItr = 0

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
        
        if idx >= 250:
            break
        print(i)

    estimateRestarts = restarts / numRuns
    estimateSteps = steps / numRuns

    return estimateRestarts, estimateSteps, convInfo