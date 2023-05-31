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
def geneticAlgorithm(population, N=8, populationSize=4, mutationRate=0.15, numRuns=100):

    convInfo = np.zeros((numRuns, 2))
    idx = 0
    totalItr = 0

    maxConflicts = utils.h(np.zeros((N,)))
    minh = maxConflicts

    for k in range(numRuns):
        weights = np.zeros((populationSize,))

        # find selection probabilities
        for i in range(populationSize):
            weights[i] = maxConflicts - utils.h(population[i])
            totalItr += 1
        weights = weights / np.linalg.norm(weights, ord=1)

        children = []

        for i in range(populationSize):
            # create a child
            inds = np.random.choice(np.linspace(0, populationSize - 1, populationSize).astype(int), p=weights, size=(2,), replace=False)
            parent1 = population[inds[0]]
            parent2 = population[inds[1]]
            child = reproduce(parent1, parent2)

            # mutate this child
            for j in range(N):
                if (np.random.uniform(low=0, high=1) < mutationRate):
                    child[j] = np.random.randint(low=0, high=N)

            children.append(child)

        population = children.copy()

        # find min h for all runs
        for i in range(populationSize):
            if utils.h(population[i]) < minh:
                minh = utils.h(population[i])

        convInfo[idx, :] = [totalItr, minh]
        idx += 1
        
    return minh, convInfo

'''
input:
    parent1: first parent for reproduction
    parent2: second parent for reproduction

returns:
    child: the reproduced child (new state)

'''
def reproduce(parent1, parent2):
    n = len(parent1)
    c = np.random.randint(low=1, high=n)
    return np.append(parent1[:c], parent2[c:])

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