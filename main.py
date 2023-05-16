import utils as utils
import math as math
import random as rand

#HELPER FUNCTION TO TRANSFORM STATE TO A 2D MATRIX REPRESENTATION
def state_representation_transform(pop):
    mat = [x[:] for x in [[0] * len(pop)] * len(pop)]
    for i in range(len(pop)):
        mat[i][pop[i]] = 1
    return mat

#HELPER FUNCTION TO DETERMINE CONFLICTS IN TWO POSITIONS
def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    print(row1, col1, row2, col2)
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
        for c2 in range(c1+1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return num_conflicts

#CREATES TUPLE --> STATE, SCORE
#PAIR[0] --> STATE 
#PAIR[1] --> SCORE
def score_tuple(state):
    score = fitness(state)
    return [state, score]

#ASSUMES THE LIST TUPLES OF STATE, SCORE IS SORTED BY SCORE IN ASCENDING ORDER
#RETURNS ONE PARENT BASED ON THE TUPLES LIST 
def roulette_selection(pairs):
    aggregate = 0.0
    for i in range(len(pairs)):
        aggregate += pairs[i][1]
        # NOTE: IT SEEMS THAT THE AGGREGATE IS STILL INITIALIZED TO ZERO 
        # DEPSITE THE FACT THAT IT SHOULD BE ADDED BEFORE HAND
    prev = 0.0
    p_state = []
    for i in range (len(pairs)):
        p_state.append(prev + (pairs[i][1] / aggregate)) 
        prev = p_state[i]
    #HERE, THE VALUE OF P_STATE[LAST] SHOULD ALWAYS BE 1. IF THIS IS NOT THE CASE
    #NOT NORMALIZED THE PROBABILITIES CORRECTLY
    r = rand.uniform(0, 1)
    for i in range (len(pairs)):
        if r < pairs[i][1]:
            temp = pairs[i]
            del pairs[i]
            return temp
            

#SINGLE POINT PIVOT CROSSOVER WHERE PIVOT IS RANDOMLY SELECTED WITH UNIFORM 
#PROBABILITY FROM THE PARENT.SIZE - 1 AVAILABLE POSITIONS
#p1 AND p2 ARE TUPLES BECAUSE I THINK IT WILL BE EASIER, NO EVIDENCE JUST A FEELING
#NOTE: NO ASEXUAL REPRODUCTION?
#NOTE: DO I VALIDATE THAT EACH CHILD MUST BE DISTINCT IMPROVEMENT UPON ITS PREVIOUS GENERATION?
#IF SO HOW MUCH TIME WOULD THAT ADD? EXPLORE AFTER THE FACT
#NOTE NO BREEDING RATE 
#IF THERE WAS A BREEDING RATE WE WRAP THE CROSSOVER IN A CONDITION UPON A RAND() < R_BREED
def breed(p1, p2):
    pivot = rand.randint(1, len(p1[0]) - 2)
    c1 = p1[0][:pivot] + p2[0][pivot:]
    c2 = p2[0][:pivot] + p1[0][pivot:]
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
    for i in range(len(c1[0])):
        if r < r_mut:
            gene_to_mutate = rand.randint(0, len(c1[0]))
            new_gene = rand.randint(0, 7)
            c1[0][gene_to_mutate] = new_gene
    return c1

def genetic_algorithm(population, r_mut, n_iter):
    [best, score] = population[0], fitness(population[0])

    for gen in range(n_iter):
        pop_scores = [fitness(population[gen]) for gen in range(len(population))]
        pop_tuples = [score_tuple(population[gen]) for gen in range(len(population))]
        #check for new best
        for i in range(len(population)):
            if pop_tuples[i][1] < score:
                [best, score] = pop_tuples[i]
                print(">%d, new best f(%s) = %f" % (gen, population[i], pop_scores[i]))
        gen2 = [roulette_selection(pop_tuples) for _ in range(len(population))]
        parents = [score_tuple(gen2[i]) for i in range(len(gen2))]
        children = list()
        for i in range(0, len(parents), 2):
            p1, p2 = parents[i], parents[i+1]
            c1, c2 = breed(p1, p2)
            c1 = random_reset_mutation(c1, r_mut)
            c2 = random_reset_mutation(c2, r_mut)
            children.append(c1)
            children.append(c2)
        population = [children[i][0] for i in range(len(children))]
        print(population)
    return [best, score]

def main():
    r_mut = 0.15
    n_iter = 1000
    population = [[rand.randint(0, 7) for _ in range(8)] for _ in range(4)]

    
    best, score = genetic_algorithm(population, r_mut, n_iter)
    print(best, score)

if __name__ == "__main__":
    main()