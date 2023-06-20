import numpy as np
import n_queens_SARR
import n_queens_GA
import n_queens_GAv2
import n_queens_GAv2_copy
import n_queens_SIM
import n_queens_PSO
import matplotlib.pyplot as plt

def main():
    maxItr = 15000
    numLoops = 50

    #convInfoSARR = n_queens_SARR.repeatSARR(maxItr, numLoops, initialState, 100, 100)
    #convInfoSIM = n_queens_SIM.repeatSIM(maxItr, numLoops, initialState, 100)
    #convInfoQSIM = n_queens_SIM.repeatSIM(maxItr, numLoops, initialState, 100, tunnelingProb=0.1)
    #convInfoPSO = n_queens_PSO.repeatPSO(maxItr, numLoops, initialState, 100)

    length = 300
    popSize = 4
    mutationRate = 0.5
    state = np.random.randint(2, size=(length,))
    population = np.random.randint(2, size=(popSize, length))
    #n_queens_SIM_copy.simulatedAnnealing(maxItr=maxItr, state=state, tunneling_prob=0.0)
    #n_queens_SARR_copy.steepestAscentRandomRestart(maxItr=maxItr, state=state)
    n_queens_GAv2_copy.geneticAlgorithm(population, N=length, populationSize=popSize, mutationRate=mutationRate, numRuns=100000)
    #convInfoGA = n_queens_GA.repeatGA(maxItr, numLoops, population=[initialState.copy() for _ in range(popSize)], numRuns=4000, mutationRate=mutationRate)
    convInfoGAv2 = n_queens_GAv2.repeatGAv2(maxItr, numLoops, population=[initialState.copy() for _ in range(popSize)], N=N, populationSize=popSize, numRuns=4000, mutationRate=mutationRate)

    fig1 = plt.figure("Figure 1")
    line1, = plt.plot(convInfoSARR[:, 0], convInfoSARR[:, 1], label='Steepest Ascent with Random Restart')
    line2, = plt.plot(convInfoSIM[:, 0], convInfoSIM[:, 1], label='Simulated Annealing')
    line3, = plt.plot(convInfoGA[:, 0], convInfoGA[:, 1], label='Genetic Algorithm Liam')
    line4, = plt.plot(convInfoGAv2[:, 0], convInfoGAv2[:, 1], label='Genetic Algorithm Gabe')
    line5, = plt.plot(convInfoQSIM[:, 0], convInfoQSIM[:, 1], label='Quantum Annealing')
    line6, = plt.plot(convInfoPSO[:, 0], convInfoPSO[:, 1], label='Particle Swarm Optimization')
    plt.legend(handles=[line1, line2, line3, line4, line5])
    plt.title('N = {} Queens, {} Max Calls, {} Iterations'.format(N, maxItr, numLoops))
    plt.xlabel("Number of Iterations")
    plt.ylabel("Average Remaining Conflicts")
    plt.grid()
    plt.show()

    return

if __name__ == "__main__":
    main()