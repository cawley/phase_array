import math as math
import random as rand

def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    
    return (row1 == row2 or                 # same row
            col1 == col2 or                 # same column 
            row1 - col1 == row2 - col2 or   # same \ diagonal
            row1 + col1 == row2 + col2)     # same / diagonal

def conflicts(state):
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1 + 1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return num_conflicts

def max_conflicts(state):
    for i in state:
        state[i] = 0
    return conflicts(state)

def fitness(state):
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1 + 1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return (max_conflicts(state) - num_conflicts)

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
    r = rand.uniform(0, 1)
    for i in range (len(population)):
        if r < p_state[i]:
            temp = population[i]
            return temp

def breed(p1, p2):
    pivot = rand.randint(1, len(p1) - 2)
    c1 = p1[:pivot] + p2[pivot:]
    c2 = p2[:pivot] + p1[pivot:]
    return [c1, c2]

def swapmutation(c1, r_mut):
    r = rand.uniform(0, 1)
    for _ in range(len(c1[0])):
        if r < r_mut:
            rpos1, rpos2 = rand.randint(0, len(c1[0])), rand.randint(0, len(c1[0]))
            temp = c1[0][rpos1]
            c1[0][rpos1] = c1[0][rpos2]
            c1[0][rpos2] = temp
    return c1

def random_reset_mutation(c1, r_mut):
    for i in range (len(c1)):
        r = rand.uniform(0, 1)
        if r < r_mut:
            new_gene = rand.randint(0, (len(c1) - 1))
            c1[i] = new_gene
    return c1

def genetic_algorithm(population, r_mut, n_iter):
    [best, score] = population[0], fitness(population[0])
    h = conflicts(population[0])
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
            if conflicts(population[i]) < h:
                h = min_h(population[i])
    print("\n", "SCORE: ", score, "\n")
    return [best, score, h]

def main():
    N = int(input("N QUEENS DEMO: Input desired dimension (N).\n"))
    size = int(input("Population size"))
    r_mut = float(input("Input Parameters: Mutation rate (default = 1/population size)"))
    n_iter = int(input("Number of Iterations"))

    population = [[rand.randint(0, N-1) for _ in range (N)] for _ in range(size)]
    state = population[0]
    score = 0
    h = conflicts(state)

    best_state = state
    best_score = score 
    best_h = h
    for _ in range(n_iter):
        best, score, h = genetic_algorithm(population, r_mut, n_iter)
        if score > best_score:
            best_score = score 
            best_state = state4

            best_h = h
    
    print("Optimal State: ", best_state, "Score: ", score, "H: ", best_h)



if __name__ == "__main__":
    main()