import math as math
import random as rand
import numpy as np

def conflict(row1, col1, row2, col2):
    return (row1 == row2 or col1 == col2 or row1 - col1 == row2 - col2 or row1 + col1 == row2 + col2)

def conflicts(state):
    N = len(state)
    return sum(conflict(state[c1], c1, state[c2], c2) for c1 in range(N) for c2 in range(c1 + 1, N))

def max_conflicts(state):
    return conflicts([0]*len(state))

def fitness(state):
    return (conflicts([0]*len(state)) - conflicts(state))

# SELECTION BASED ON FITNESS PROPORTIONATE ROULETTE 
# https://en.wikipedia.org/wiki/Fitness_proportionate_selection
def roulette_selection(population, scores):
    #population.sort(key = fitness, reverse = True)
    aggregate = 0.0
    for i in range(len(population)):
        aggregate += scores[i]
    prev = 0.0
    p_state = []
    for i in range (len(population)):
        if aggregate != 0:
            p_state.append(prev + (scores[i] / aggregate)) 
        else:
            p_state.append(prev)
        prev = p_state[i]
    r = rand.uniform(0, 1)
    for i in range (len(population)):
        if r < p_state[i]:
            temp = population[i]
            return temp

# SINGLE POINT CROSSOVER BREEDING
# https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
def breed(p1, p2):
    pivot = rand.randint(1, len(p1) - 2)
    c1 = np.append(p1[:pivot], p2[pivot:])
    c2 = np.append(p2[:pivot], p1[pivot:])
    return [c1, c2]

# SWAP MUTATION GA
# https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)
def swapmutation(c1, r_mut):
    r = rand.uniform(0, 1)
    for _ in range(len(c1[0])):
        if r < r_mut:
            rpos1, rpos2 = rand.randint(0, len(c1[0])), rand.randint(0, len(c1[0]))
            temp = c1[0][rpos1]
            c1[0][rpos1] = c1[0][rpos2]
            c1[0][rpos2] = temp
    return c1

# RANDOM RESET MUTATION
# https://www.geeksforgeeks.org/mutation-algorithms-for-string-manipulation-ga/
def random_reset_mutation(c1, r_mut):
    for i in range (len(c1)):
        r = rand.uniform(0, 1)
        if r < r_mut:
            new_gene = rand.randint(0, (len(c1) - 1))
            c1[i] = new_gene
    return c1

# STANDARD GA FOR N QUEENS WITH ALL PARAMS MENTIONED  
def genetic_algorithm(population, r_mut, n_iter):
    convInfo = np.zeros((n_iter, 2))
    idx = 0
    totalItr = 0

    [best, score] = population[0], fitness(population[0])
    h = conflicts(population[0])
    for gen in range(n_iter):
        T = gen == 0 and 1 or (1/gen)
        r = rand.uniform(0, 1)

        scores = [fitness(population[i]) for i in range(len(population))]
        totalItr += len(population)
        #check for new best
        for i in range(len(population)):
            if scores[i] > score:
                best, score = population[i], scores[i]
                #print(">%d, new best f(%s) = %f" % (gen, population[i], scores[i]))

        if r < T:
            parents = [roulette_selection(population, scores) for _ in range(len(population))]
        else:
            parents = population.copy()
        
        children = list()
        for i in range(0, len(parents) - 1, 2):
            p1, p2 = parents[i], parents[i+1] 
            c1, c2 = breed(p1, p2)
            c1 = random_reset_mutation(c1, r_mut)
            c2 = random_reset_mutation(c2, r_mut)
            children.append(c1)
            children.append(c2)
        population = children.copy()
        for i in range(len(population)):
            if conflicts(population[i]) < h:
                h = conflicts(population[i])

        convInfo[idx, :] = [totalItr, h]
        idx += 1
        if max_conflicts(population[0]) == score:
            return [best, score, h], convInfo
    return [best, score, h], convInfo

def main():
    print("read comments for parameter explanation\n")
    N = int(input("N"))             #BOARD SIZE/QUEEN COUNT: THE (N) IN NQUEENS
    size = int(input("SIZE"))       #POPULATION SIZE: HOW MANY CANDIDATE STATES ARE CONSIDERED?
    r_mut = float(input("R_MUT"))   #MUTATION RATE (FLOAT BETWEEN 0 AND 1)
    n_iter = int(input("N_ITER"))   #NUMBER OF ITERATIONS PER ALGORITHM RUN
    n_samp = int(input("N_SAMP"))   #NUMBER OF TRIALS WHERE ONE TRIAL IS N_ITER ITERATIONS OF GA

    population = [[rand.randint(0, N-1) for _ in range (N)] for _ in range(size)]

    state = population[0]
    score = 0

    best_state = state
    best_score = score 

    totalh = 0
    for _ in range(n_samp):
        best, score, h = genetic_algorithm(population, r_mut, n_iter)
        totalh += h
        if score > best_score:
            best_score = score 
            best_state = state
    
    totalh = totalh / n_samp

    print("Max Possible Score: ", max_conflicts(best_state), "Best State:", best_state, "Best Score:", score, "H:", totalh)

'''
input:
    maxItr: max number of obj fn calls
    numLoops: number of loops to average over
    population: initial state population
    mutationRate: rate of mutation
    numRuns: number of runs

returns:
  convInfo: (n x 2) matrix of minimum conflicts and number of objective function calls, averaged over numLoops calls

'''
def repeatGA(maxItr, numLoops, population, mutationRate=0.15, numRuns=100):
    numRuns = maxItr // np.shape(population)[0]
    minh, convInfoFinal = genetic_algorithm(population, mutationRate, numRuns)
    print("Repeat GA")
    for i in range(numLoops - 1):
        minh, convInfo = genetic_algorithm(population, mutationRate, numRuns)

        convInfoFinal += convInfo
        print(i)
    
    convInfoFinal /= numLoops

    return convInfoFinal

if __name__ == "__main__":
    main()