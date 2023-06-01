import numpy as np
import random as rand
from matplotlib import pyplot as plt
import json

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_arr = np.fromstring(opt_str, dtype=int, sep = ' ')
inpfile = open("in.txt", "r")
inp_str = inpfile.read()
inp_arr = np.fromstring(inp_str, dtype=int, sep = ' ')

def generate_bin():
    f = open("in.txt", "w")
    c = 1
    for _ in range(256):
        s = ""
        for _ in range(6):
            r = rand.uniform(0, 1)
            if r > .5:
                s += "1"
            else:
                s += "0"        
        f.write(s)
        f.write(" ")
        c +=1

def objective(state):
    return np.sum(state != opt_string)

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

def main():
    generate_bin()
    state = inp_str
    n_iter = 100
    n_samp = 10

    outfile = open("out.txt", "w")
    outfile.write(inp_str)
    outfile.write(opt_str)
    print(inp_arr)
    print(opt_arr)

    ci_sarr = repeatSARR(n_iter, n_samp, state, 100, 100)
    line1, = plt.plot(ci_sarr[:, 0], convInfoSARR[:, 1], label='Steepest Ascent with Random Restart')
    plt.legend(handles=[line1])
    plt.title('N = {} Queens, {} Max Calls, {} Iterations'.format(N, maxItr, numLoops))
    plt.xlabel("Number of Iterations")
    plt.ylabel("Average Remaining Conflicts")
    plt.grid()
    plt.show()

#opt_arr_str = ['{:06b}'.format(num) for num in opt_arr]



if __name__ == "__main__":
    main()