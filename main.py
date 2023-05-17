import utils as utils
import math as math
import random as rand

#HELPER FUNCTION TO DETERMINE CONFLICTS IN TWO POSITIONS
def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    
    return (row1 == row2 or                 # same row
            col1 == col2 or                 # same column 
            row1 - col1 == row2 - col2 or   # same \ diagonal
            row1 + col1 == row2 + col2)     # same / diagonal

#FITNESS EVALUATION FUNCTION. WE ARE MINIMIZING NUM_CONFLICTS THEREBY CHOOSING THE 
#STATE THAT HAS THE LOWEST CORRESPONDING OBJECTIVE VALUE
#INPUT: STATE 1D LIST OUTPUT: SCORE ASSOCIATED WITH A SPECIFIC STATE
def fitness(state):
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1 + 1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return (28 - num_conflicts)

def min_h(state):
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1 + 1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return num_conflicts

#RETURNS ONE PARENT BASED ON THE SCORES LIST 
#TAKES A POPULATION OF CANDIDATE STATES RETURNS THE R.S. FIRST SELECTION 
def roulette_selection(population, scores):
    population.sort(key = fitness, reverse = True)
    aggregate = 0.0
    for i in range(len(population)):
        aggregate += scores[i]
    prev = 0.0
    p_state = []
    for i in range (len(population)):
        p_state.append(prev + (scores[i] / aggregate)) 
        prev = p_state[i]
    #HERE, THE VALUE OF P_STATE[LAST] SHOULD ALWAYS BE 1. IF THIS IS NOT THE CASE
    #NOT NORMALIZED THE PROBABILITIES CORRECTLY
    r = rand.uniform(0, 1)
    for i in range (len(population)):
        if r < p_state[i]:
            temp = population[i]
            #del population[i]
            return temp

#SINGLE POINT PIVOT CROSSOVER WHERE PIVOT IS RANDOMLY SELECTED WITH UNIFORM 
#PROBABILITY FROM THE PARENT.SIZE - 1 AVAILABLE POSITIONS
#p1 AND p2 ARE TUPLES BECAUSE I THINK IT WILL BE EASIER, NO EVIDENCE JUST A FEELING
#NOTE THEY ARE NO LONGER TUPLES IT WAS NOT EASIER
#NOTE: NO ASEXUAL REPRODUCTION?
#NOTE: DO I VALIDATE THAT EACH CHILD MUST BE DISTINCT IMPROVEMENT UPON ITS PREVIOUS GENERATION?
#IF SO HOW MUCH TIME WOULD THAT ADD? EXPLORE AFTER THE FACT
#NOTE NO BREEDING RATE 
#IF THERE WAS A BREEDING RATE WE WRAP THE CROSSOVER IN A CONDITION UPON A RAND() < R_BREED
def breed(p1, p2):
    pivot = rand.randint(1, len(p1) - 2)
    c1 = p1[:pivot] + p2[pivot:]
    c2 = p2[:pivot] + p1[pivot:]
    return [c1, c2]


#HERE WE EMPLOY A SWAP MUTATION 
# BY TWO RANDOMLY SELECTED POSITIONS IN THE LIST
def swapmutation(c1, r_mut):
    r = rand.uniform(0, 1)
    for _ in range(len(c1[0])):
        if r < r_mut:
            rpos1, rpos2 = rand.randint(0, len(c1[0])), rand.randint(0, len(c1[0]))
            temp = c1[0][rpos1]
            c1[0][rpos1] = c1[0][rpos2]
            c1[0][rpos2] = temp
    return c1

#HERE IS EMPLOYED RANDOM RESET MUTATION BECAUSE IT SEEMS THAT SWAPMUTATION IS
#NOT SUITABLE FOR THIS [IMPLEMENTATION]
#INPUT IS A TUPLE
def random_reset_mutation(c1, r_mut):
	r = rand.uniform(0, 1)
	for _ in range (len(c1)):
		if r < r_mut:
			gene_to_mutate = rand.randint(0, len(c1) - 1)
			new_gene = rand.randint(0, 7)
			c1[gene_to_mutate] = new_gene
	return c1
master_list = []
def genetic_algorithm(population, r_mut, n_iter):
    [best, score] = population[0], fitness(population[0])
    for gen in range(n_iter):
        scores = [fitness(population[gen]) for gen in range(len(population))]
        #check for new best
        for i in range(len(population)):
            if scores[i] > score:
                best, score = population[i], scores[i]
                print(">%d, new best f(%s) = %f" % (gen, population[i], scores[i]))
        parents = [roulette_selection(population, scores) for _ in range(len(population))]
        children = list()
        for i in range(0, len(parents) - 1, 2):
            p1, p2 = parents[i], parents[i+1]
            c1, c2 = breed(p1, p2)
            c1 = random_reset_mutation(c1, r_mut)
            c2 = random_reset_mutation(c2, r_mut)
            children.append(c1)
            children.append(c2)
        population = children
        for i in range(len(population)):
            master_list.append(min_h(population[i]))
    print("\n", "SCORE: ", score, "\n")
    return [best, score]

def main():
    r_mut = 0.15
    n_iter = 1000
    population = [[rand.randint(0, 7) for _ in range(8)] for _ in range(4)]

    total = 0
    master = []
    for _ in range(1000):
        best, score = genetic_algorithm(population, r_mut, n_iter)
        master.append(master_list)
        total += score
    print(total/1000)

    new_total = 0
    for i in master_list:
        for j in i:
            new_total += j
    print("\n\n")
    print(j/1000)

if __name__ == "__main__":
    main()