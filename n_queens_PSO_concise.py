import random as rand
import numpy as np

def conflict(row1, col1, row2, col2):
    return (row1 == row2 or col1 == col2 or row1 - col1 == row2 - col2 or row1 + col1 == row2 + col2)

def conflicts(state):
    N = len(state)
    return sum(conflict(state[c1], c1, state[c2], c2) for c1 in range(N) for c2 in range(c1 + 1, N))

def fitness(state):
    return (conflicts([0]*len(state)) - conflicts(state))

global gbest
global gbest_score

def pso(n_sub, n_parts, r_maxv, n_iter, cognitive, social, inertia):
    gbest = [-1]*n_sub 
    gbest_score = -np.inf

    particles = [{'states': [rand.randint(0, n_parts-1) for _ in range(n_sub)],
                  'pbest': [-1]*n_sub,
                  'pbest_score': 0,
                  'v': [rand.randint(0, r_maxv) for _ in range(n_sub)]} for _ in range(n_sub)]
    h = conflicts(particles[0]['states'])
    for i in range(n_iter):
        for particle in particles:
            score = fitness(particle['states'])
            particle['score'] = score
            if score > particle['pbest_score']:
                particle['pbest'] = particle['states'].copy()
                particle['pbest_score'] = score

            if score > gbest_score:
                gbest = particle['states'].copy()
                gbest_score = score

            for particle_idx, particle in enumerate(particles):
                for state_idx, state_val in enumerate(particle['states']):
                    r = rand.randint(0, 2)
                    particle['states'][state_idx] = inertia * particle['v'][state_idx] + cognitive * r * (particle['pbest'][state_idx] - state_val) + social * r * (gbest[state_idx] - state_val)
                    particle['states'][state_idx] = (particle['states'][state_idx] + particle['v'][state_idx]) % n_sub
        
        for j in range(len(particles)):
            if conflicts(particles[j]['states']) < h:
                h = conflicts(particles[j]['states'])
            print(particles[j])

        print(f"Global Best: {gbest} Score: {gbest_score}\n")

    return gbest, h

def main():
    n_sub = int(input("N (Queens)")) 
    n_parts = int(input("Swarm Quantity"))
    r_maxv = int(input("Max Velocity"))
    n_iter = int(input("Iteration Count"))
    n_samp = int(input("Amount of Trials"))

    cognitive = 1
    social = 1
    inertia = 2

    g, h = pso(n_sub, n_parts, r_maxv, n_iter, cognitive, social, inertia)

    print("Max Score Possible for N queens", conflicts([0]*len(g)))
    print("Best State:", g, "Best State Score:", fitness(g))

    totalh = 0
    for i in range(n_samp):
        g, h = pso(n_sub, n_parts, r_maxv, n_iter, cognitive, social, inertia)
        totalh += h
    print(f"H Score: {totalh/n_samp}")

if __name__ == "__main__":
    main()
