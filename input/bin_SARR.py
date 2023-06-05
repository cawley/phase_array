import numpy as np
import random as rand
from matplotlib import pyplot as plt
import distance as ds

optfile = open("optimal_state.txt", "r")
opt_str = optfile.read()
opt_lst = list(opt_str)
opt_arr = [i for i in opt_lst if (i == '0' or i == '1')]

inpfile = open("in.txt", "r")
inp_str = inpfile.read()

def generate_random_binary_string(n):
    return ''.join(rand.choice('01') for _ in range(n))

state_str = generate_random_binary_string(len(opt_arr))
state = list(state_str)

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
    return ds.levenshtein(state, opt_arr)

def steepestAscent(state, convInfo, idx, totalItr, minh):
    state = list(state)

    current = state
    count = 0

    while True:
        neighbor = current
        neighborH = -objective(current)
        N = len(current)

        #find best neighbor
        for i in range(N):
            temp = current

            # move down
            while (temp[i] == '0'):
                totalItr += 1
                temp[i] = '1'
                if -objective(temp) > neighborH:
                    neighbor = temp
                    neighborH = -objective(temp)

            # move up
            while (temp[i] == '1'):
                totalItr += 1
                temp[i] += '0'
                if -objective(temp) > neighborH:
                    neighbor = temp
                    neighborH = -objective(temp)

        if neighborH <= -objective(current):
            return current, objective(state), objective(current), count, convInfo, idx, totalItr, minh
        

        current = neighbor
        count += 1

        if objective(current) < minh:
            minh = objective(current)

        convInfo[idx, :] = [totalItr, minh]
        idx += 1

def steepestAscentRandomRestart(maxItr, state, numRuns=10, numRestarts=10):

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
        state_str = generate_random_binary_string(len(opt_arr))
        state = list(state_str)
        for j in range(numRestarts):
            arr, hInitial, currH, count, convInfo, idx, totalItr, minh = steepestAscent(state, convInfo, idx, totalItr, minh)
            steps += count

            # check if the problem is solved
            if currH == 0:
                break
            else:
                # randomize the state
                state_str = generate_random_binary_string(len(opt_arr))
                state = list(state_str)

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
    n_iter = 10
    n_samp = 10

    print(objective(state))

    ci_sarr = repeatSARR(n_iter, n_samp, state, 10, 10)
    print(ci_sarr)
    #line1, = plt.plot(ci_sarr[:, 0], ci_sarr[:, 1], label='Steepest Ascent with Random Restart')
    #plt.legend(handles=[line1])
    #plt.title('N = {} Queens, {} Max Calls, {} Iterations'.format(N, maxItr, numLoops))
    #plt.xlabel("Number of Iterations")
    #plt.ylabel("Average Remaining Conflicts")
    #plt.grid()
    #plt.show()




if __name__ == "__main__":
    main()
# May Be Useful Later
#from difflib import SequenceMatcher
#from Bio.Align import PairwiseAligner
#return SequenceMatcher(None, state, opt_str).ratio()
#return PairwiseAligner.score(state, opt_arr)
#opt_arr_str = ['{:06b}'.format(num) for num in opt_arr]
