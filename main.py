import utils
import numpy as np
import tensorflow as tf
import test as test

'''
def main():
    #state = [1, 0, 0, 3, 4, 5, 1, 6]
  
    #result_5_1 = utils.steepestAscent(state)

    #result_5_2 = utils.steepestAscentRandomRestart(state)

    totalh = 0
    for i in range(1000):
        totalh += utils.geneticAlgorithm()
        print(i)
    result_5_3 = totalh / 1000 # should be close to 2.33
    print(result_5_3)
    return
'''
    
def main():
    #hyperparameters
    n_pop = 4 #population size
    n_bits = 8 #single candidate solution size
    n_iter = 100 #algorithm iterations
    r_cross = 0.85
    r_mut = 0.15

    agg = 0
    best = 0 #best state arrangement
    cbest = 0 #current best score

    #initial population given in 5.3
    pop = [1, 0, 0, 3, 4, 5, 1, 6]

    for i in range(1000):
        t1, t2 = test.genetic_algorithm(pop, utils.h, n_bits, n_iter, n_pop, r_cross, r_mut)
        if t2 > cbest:
            best = t1
        agg += t2
    print (agg / 1000)
    
    print(best, cbest)
    
    return;


if __name__=="__main__":
    main()
