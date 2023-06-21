import numpy as np
import utils

'''
input:
    population: initial state population
    N: number of queens
    populationSize: size of the population
    mutationRate: rate of mutation
    numRuns: number of runs

returns:
    minh: minimum h value over all (populationSize * runRuns) states
    convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls, averaged over numLoops calls

'''
def geneticAlgorithm(population, N=8, populationSize=4, mutationRate=0.15, numRuns=10000):
    M, N = np.shape(population[0])

    convInfo = np.zeros((numRuns, 2))
    idx = 0
    totalItr = 0

    maxh = utils.h_dec(population[0])

    for k in range(numRuns):
        weights = np.zeros((populationSize,))

        # find selection probabilities
        for i in range(populationSize):
            weights[i] = utils.h_dec(population[i])
        
            totalItr += 1

        max_val = np.max(weights)
        max_ind = np.argmax(weights)
        super_child = population[max_ind]

        print('Run: {}, h: {}'.format(totalItr, max_val))

        if max_val >= M * N - 1:
            print(super_child)
            return
        weights = np.power(weights, 3)
        weights = weights / np.linalg.norm(weights, ord=1)

        children = [None] * populationSize

        for i in range(populationSize - 1):
            # create a child
            inds = np.random.choice(np.linspace(0, populationSize - 1, populationSize).astype(int), p=weights, size=(2,), replace=False)
            parent1 = population[inds[0]]
            parent2 = population[inds[1]]
            child = reproduce(parent1, parent2)

            mutationRate = (M * N - max_val) / (M * N)
            # mutate this child
            for j in range(M):
                for k in range(N):
                    if (np.random.uniform(low=0, high=1) < mutationRate):
                        if (np.random.uniform(low=0, high=1)) < 0.5:
                            if child[j, k] >= 0:
                                child[j, k] -= 1 / 64
                        else:
                            if child[j, k] <= 1:
                                child[j, k] += 1 / 64

            children[i] = child
        children[-1] = super_child

        population = children.copy()

        # find min h for all runs
        #for i in range(populationSize):
        #    if utils.h2(population[i]) < minh:
        #        minh = utils.h2(population[i])

        convInfo[idx, :] = [totalItr, maxh]
        idx += 1
        
    return maxh, convInfo

'''
input:
    parent1: first parent for reproduction
    parent2: second parent for reproduction

returns:
    child: the reproduced child (new state)

'''
def reproduce(parent1, parent2):
    M, N = np.shape(parent1)
    flat1 = parent1.flatten()
    flat2 = parent2.flatten()
    n = len(flat1)
    inds = np.random.choice(np.linspace(0, n - 1, n).astype(int), size=(int(n / 2),), replace=False)
    for ind in inds:
        flat2[ind] = flat1[ind]
    return np.reshape(flat2, (M, N))

'''
input:
    maxItr: max number of obj fn calls
    numLoops: number of loops to average over
    population: initial state population
    N: number of queens
    populationSize: size of the population
    mutationRate: rate of mutation
    numRuns: number of runs

returns:
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls, averaged over numLoops calls

'''
def repeatGAv2(maxItr, numLoops, population, N=8, populationSize=4, mutationRate=0.15, numRuns=100):
    numRuns = maxItr // populationSize
    minh, convInfoFinal = geneticAlgorithm(population, N, populationSize, mutationRate, numRuns)
    print("Repeat GAv2")
    for i in range(numLoops - 1):
        minh, convInfo = geneticAlgorithm(population, N, populationSize, mutationRate, numRuns)

        convInfoFinal += convInfo
        print(i)
    
    convInfoFinal /= numLoops

    return convInfoFinal