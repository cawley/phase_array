# phase_array
### Hi! :blush: Welcome to the phase_array README.md! 😲 We hope this helps! 😆
This repository represents an attempt at general solution to optimal arrangement of nodes in a hypothetical phase array.
We reduce this problem (a lot) to a famous, easy-to-grasp and NP-hard one dimensional optimization problem NQueens. 
We attempt this problem with a few different metaheuristics:
  - Genetic Algorithm
  - Particle Swarm Optimization
  - Simulated Annealing
  - Steepest Ascent
  - Steepest Ascent with Random Restart
  - Quantum Annealing

We then rate the performance of each implementation, where a high performance is denoted by a low number of calls to the fitness function and tendency towards the optimal state as N tends to the highest known solution for NQueens, 27.
Following are explanations for the usage and understanding of each algorithm. 

## Queens PSO Optimization README
## Description
This script uses the Particle Swarm Optimization (PSO) algorithm to solve the N-Queens problem. The N-Queens problem is a classic AI problem where one is asked to place N queens on an NxN chess board such that no two queens threaten each other. This problem is famous for its NP-Hard nature. The goal of this script is to provide an optimized solution for the problem using PSO.

The PSO algorithm is an optimization technique that works by having a population (known as a swarm) of candidate solutions (known as particles). These particles move around in the search space according to some simple formulae. The movements of the particles are guided by their own best known position along with the swarm's overall best known position. Over time, the swarm as a whole, like birds flocking or fish schooling, will tend towards an optimal area of the search space.

### How it Works
The script generates an initial population (swarm) of random solutions (particles). Each particle is evaluated for fitness (its conflicts with other particles) using the fitness function.

The algorithm iteratively updates the velocity and position of each particle towards its personal best position and the global best position found in the entire swarm. The position updating is weighted by three parameters: cognitive, social, and inertia.

The gbest and gbest_score variables store the best found position (solution) and its score. Each particle also keeps track of its own best position (pbest) and score (pbest_score).

The algorithm stops iterating once a maximum number of iterations n_iter is reached. The output is the best solution found (gbest) and its fitness score (h).

# Code Structure
The main function main handles user input and calls the pso function with the appropriate parameters. The pso function runs the actual PSO algorithm. Auxiliary functions include conflict and conflicts which are used to calculate the fitness of a given state.

# Inputs and Outputs
**conflict**: It checks if there is a conflict between two queens on the board.

**Input**: row1, col1, row2, col2 representing the positions of two queens.

**Output**: Returns True if there is a conflict, False otherwise.

**conflicts**: It calculates the total number of conflicts in the given state of the board.

**Input**: state representing a state of the board.
**Output**: Returns the number of conflicts.

fitness: It calculates the fitness of a given state.

Input: state representing a state of the board.
Output: Returns the fitness value, calculated as the difference between the number of conflicts in an initial state (with all queens on the first row) and the number of conflicts in the given state.

pso: It runs the PSO algorithm.

Inputs: n_sub (number of subparticles), n_parts (number of particles per swarm), r_maxv (max velocity), n_iter (number of iterations), cognitive, social, inertia (weights).
Outputs: Returns gbest (best state found) and h (minimum fitness found).
main: It handles user input and runs the pso function.

Input: Takes input from user for n_sub, n_parts, r_maxv, n_iter and n_samp.
Output: Prints the best state found and its fitness score.

Usage
Run the script in a Python environment.
When prompted, input the following parameters: n_sub, n_parts, r_maxv, n_iter and n_samp.
The script will output the best state found and its fitness score.
For multiple trials, the script will also output an average h-score.

License
This project is licensed under the MIT License.
