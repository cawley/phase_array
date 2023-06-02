import numpy as np
import random as rand
from difflib import SequenceMatcher as sm 
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import time

def conflict(row1, col1, row2, col2):
    return (row1 == row2 or col1 == col2 or row1 - col1 == row2 - col2 or row1 + col1 == row2 + col2)

def conflicts(state):
    N = len(state)
    return sum(conflict(state[c1], c1, state[c2], c2) for c1 in range(N) for c2 in range(c1 + 1, N))

def objective(state):
    return (conflicts([0]*len(state)) - conflicts(state))    

def steepestAscent(state, convInfo, idx, totalItr, minh):

    current = state.copy()
    count = 0

    while True:
        neighbor = current.copy()
        neighborH = -objective(current)
        N = len(current)

        #find best neighbor
        for i in range(N):
            temp = current.copy()

            # move down
            while (temp[i] != 0):
                totalItr += 1
                temp[i] -= 1
                if -objective(temp) > neighborH:
                    neighbor = temp.copy()
                    neighborH = -objective(temp)

            # move up
            while (temp[i] != N - 1):
                totalItr += 1
                temp[i] += 1
                if -objective(temp) > neighborH:
                    neighbor = temp.copy()
                    neighborH = -objective(temp)

        if neighborH <= -objective(current):
            return current, objective(state), objective(current), count, convInfo, idx, totalItr, minh
        

        current = neighbor.copy()
        count += 1

        if objective(current) < minh:
            minh = objective(current)

        convInfo[idx, :] = [totalItr, minh]
        idx += 1

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

def steepestAscentRandomRestart(maxItr, state, numRuns=1000, numRestarts=100):

    convInfo = np.zeros((10000, 2))
    idx = 0

    N = len(state)

    maxConflicts = objective(np.zeros((N,)))
    minh = objective(state)

    restarts = 0
    steps = 0
    totalItr = 0

    convInfo[idx, :] = [totalItr, minh]
    idx += 1
    totalItr += 1

    for j in range(numRestarts):
        arr, hInitial, currH, count, convInfo, idx, totalItr, minh = steepestAscent(state, convInfo, idx, totalItr, minh)
        steps += count

        # check if the problem is solved
        if currH == 0:
            return restarts, steps, convInfo, idx
        else:
            # randomize the state
            state = np.random.randint(low=0, high=N, size=(N,))

        restarts += 1
    
    return restarts, steps, convInfo, idx

def parallel_steepestAscentRandomRestart(maxItr, state, numRuns=1000, numRestarts=100):
    # determine the number of workers, which typically equal to the number of cores 
    num_workers = 8 # adjust the number based on your machine

    # create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # start the tasks and get the futures
        futures = [executor.submit(steepestAscentRandomRestart, maxItr, state, numRestarts) for _ in range(numRuns)]
        
        results = []
        # gather the results as they become available
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    return results

def main():
    n_iter = 100
    state = [1,2,3,4,5,6,7,0]
    runs = 1000
    restarts = 100
    test = parallel_steepestAscentRandomRestart(n_iter, state, runs, restarts)

    

if __name__ == "__main__":
    main()