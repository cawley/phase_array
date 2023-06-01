utils:

steepestAscent(state)
'''
input: initial state

returns:
    current: the final state
    h: the heuristic cost of the final state
    count: the number of steps taken

'''

steepestAscentRandomRestart(state, numRuns=1000, numRestarts=100)
'''
input: 
    state: initial state
    runRuns: number of runs
    rumRestarts: number of restarts

returns:
    estimateRestarts: Empirical estimate of the expected number of restarts
    estimateSteps: Empirical estimate of the expected total number of steps across restarts

'''

geneticAlgorithm(N=8, populationSize=4, mutationRate=0.15, numRuns=100)
'''
input:
    N: number of queens
    populationSize: size of the population
    mutationRate: rate of mutation
    numRuns: number of runs

returns:
    minh: minimum h value over all (populationSize * runRuns) states
'''

main:
	
runs steepestAscent for 5.1, runs steepestAscentRandomRestart for 5.2, runs geneticAlgorithm 1000 times and keeps track of average min h across 1000 runs for 5.3.