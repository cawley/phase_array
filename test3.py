import utils as utils
import math as math
import random as rand

#HELPER FUNCTION TO TRANSFORM STATE TO A 2D MATRIX REPRESENTATION
def state_representation_transform(pop):
    mat = [x[:] for x in [[0] * len(pop)] * len(pop)]
    for i in range(len(pop)):
        mat[i][pop[i]] = 1
    return mat

#HELPER FUNCTION TO DETERMINE CONFLICTS IN ROWS
def conflict(row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    return (row1 == row2 or  # same row
            col1 == col2 or  # same column
            row1 - col1 == row2 - col2 or  # same \ diagonal
            row1 + col1 == row2 + col2)  # same / diagonal

#FITNESS EVALUATION FUNCTION. WE ARE MINIMIZING NUM_CONFLICTS THEREBY CHOOSING THE 
#STATE THAT HAS THE LOWEST CORRESPONDING OBJECTIVE VALUE
#INPUT: STATE 1D LIST OUTPUT: SCORE ASSOCIATED WITH A SPECIFIC STATE
def objective(state):
    num_conflicts = 0
    N = len(state)
    for c1 in range(N):
        for c2 in range(c1+1, N):
            num_conflicts += conflict(state[c1], c1, state[c2], c2)
    return num_conflicts

def score_tuple(state):
    #TODO
    #CREATE A LIST OF TUPLE WITH EACH STATE AND ITS CORRESPONDING SCORE
    return

#ASSUMES THE LIST TUPLES OF STATE, SCORE IS SORTED BY SCORE IN ASCENDING ORDER
#RETURNS ONE PARENT BASED ON THE TUPLES LIST 
def roulette_selection(tuples):
    sum = 0.0
    for i in range(len(tuples)):
        sum += tuples[i].second
    prev = 0.0
    p_state = []
    for i in range (4):
        p_state[i] = prev + (tuples[i].second / sum)
        prev = p_state[i]
    #HERE, THE VALUE OF P_STATE[LAST] SHOULD ALWAYS BE 1. IF THIS IS NOT THE CASE
    #NOT NORMALIZED THE PROBABILITIES CORRECTLY
    r = rand.uniform(0, 1)
    if r < tuples[0].second: 
        return 
