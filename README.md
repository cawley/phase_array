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

# Genetic Algorithm Approach 

## Description
This script uses the Genetic Algorithm (GA) to solve the N-Queens problem. The N-Queens problem is a classic artificial intelligence problem where one is asked to place N queens on an NxN chess board such that no two queens threaten each other. The Genetic Algorithm is a search heuristic that is inspired by Charles Darwin’s theory of natural evolution. This algorithm reflects the process of natural selection where the fittest individuals are selected for reproduction in order to produce the offspring of the next generation.

## How it Works
The script uses a population of possible solutions to the N-Queens problem. Each individual in the population is a possible solution to the problem. The individuals are then evolved towards an optimal or near-optimal solution over successive generations. Each generation applies the principles of survival of the fittest, genetic crossover (breeding), and mutation to create a new population. This new population is then used in the next iteration of the algorithm.

Fitness is calculated as the difference between the maximum number of conflicts possible and the actual number of conflicts in a given state. The fewer conflicts, the fitter the individual.

The script uses roulette wheel selection to select individuals for breeding based on their fitness. Two individuals are then bred using single point crossover. The offspring produced by breeding undergo mutation with a certain probability. The mutations can be either swap mutations, where two genes (queen positions) are swapped, or random reset mutations, where a gene is replaced with a random value.

This process is repeated for a given number of iterations, and the best solution found over all iterations is returned.

## Code Structure
The main function `main` handles user input and calls the `genetic_algorithm` function with the appropriate parameters. The `genetic_algorithm` function runs the actual Genetic Algorithm. Auxiliary functions include `conflict`, `conflicts`, `max_conflicts`, `fitness`, `roulette_selection`, `breed`, `swapmutation`, and `random_reset_mutation`.

## Inputs and Outputs
1. **conflict**: Checks if there is a conflict between two queens.
    - Input: `row1, col1, row2, col2` representing the positions of two queens.
    - Output: Returns 1 if there is a conflict, 0 otherwise.

2. **conflicts**: Calculates the total number of conflicts in the given state of the board.
    - Input: `state` representing a state of the board.
    - Output: Returns the number of conflicts.

3. **max_conflicts**: Calculates the maximum possible conflicts in the given state of the board.
    - Input: `state` representing a state of the board.
    - Output: Returns the maximum number of conflicts.

4. **fitness**: Calculates the fitness of a given state.
    - Input: `state` representing a state of the board.
    - Output: Returns the fitness value.

5. **roulette_selection**: Selects an individual from a population based on fitness.
    - Input: `population` representing a population of individuals, `scores` representing the fitness scores of the individuals.
    - Output: Returns a selected individual.

6. **breed**: Breeds two individuals to create two offspring.
    - Input: `p1, p2` representing two parent individuals.
    - Output: Returns two offspring individuals.

7. **swapmutation**: Performs swap mutation on an individual.
    - Input: `c1` representing an individual, `r_mut` representing the mutation rate.
    - Output: Returns the mutated individual.

8. **random_reset_mutation**: Performs random reset mutation on an individual.
    - Input: `c1` representing an individual, `r_mut` representing the mutation rate.
    - Output: Returns the mutated individual.

9. **genetic_algorithm**: Executes the genetic algorithm to solve the N-Queens problem.
    - Input: `population` representing a population of individuals, `r_mut` representing the mutation rate, `n_iter` representing the number of iterations.
    - Output: Returns the best state, its score, and the h score.

## Execution
1. Run the script in a Python environment.
2. When prompted, input the following parameters: `N`, `size`, `r_mut`, `n_iter`, and `n_samp`.
3. The script will output the best state found and its score.

## License
This project is licensed under the MIT License.

# Particle Swarm Optimization Approach 
## Description
This script uses the Particle Swarm Optimization (PSO) algorithm to solve the N-Queens problem. The N-Queens problem is a classic AI problem where one is asked to place N queens on an NxN chess board such that no two queens threaten each other. This problem is famous for its NP-Hard nature. The goal of this script is to provide an optimized solution for the problem using PSO.

The PSO algorithm is an optimization technique that works by having a population (known as a swarm) of candidate solutions (known as particles). These particles move around in the search space according to some simple formulae. The movements of the particles are guided by their own best known position along with the swarm's overall best known position. Over time, the swarm as a whole, like birds flocking or fish schooling, will tend towards an optimal area of the search space.

## How it Works
The script generates an initial population (swarm) of random solutions (particles). Each particle is evaluated for fitness (its conflicts with other particles) using the fitness function.

The algorithm iteratively updates the velocity and position of each particle towards its personal best position and the global best position found in the entire swarm. The position updating is weighted by three parameters: cognitive, social, and inertia.

The gbest and gbest_score variables store the best found position (solution) and its score. Each particle also keeps track of its own best position (pbest) and score (pbest_score).

The algorithm stops iterating once a maximum number of iterations n_iter is reached. The output is the best solution found (gbest) and its fitness score (h).

## Code Structure
The main function main handles user input and calls the pso function with the appropriate parameters. The pso function runs the actual PSO algorithm. Auxiliary functions include conflict and conflicts which are used to calculate the fitness of a given state.

## Inputs and Outputs
1. **conflict**: Checks if there is a conflict between two queens.
    - Input: `row1, col1, row2, col2` representing the positions of two queens.
    - Output: Returns 1 if there is a conflict, 0 otherwise.

2. **conflicts**: Calculates the total number of conflicts in the given state of the board.
    - Input: `state` representing a state of the board.
    - Output: Returns the number of conflicts.

3. **max_conflicts**: Calculates the maximum possible conflicts in the given state of the board.
    - Input: `state` representing a state of the board.
    - Output: Returns the maximum number of conflicts.

4. **fitness**: Calculates the fitness of a given state.
    - Input: `state` representing a state of the board.
    - Output: Returns the fitness value.

5. **pso**: It runs the **PSO** algorithm. 
    - Inputs: `n_sub` (number of subparticles), `n_parts` (number of particles per swarm), `r_maxv` (max velocity), `n_iter` (number of iterations), `cognitive`, `social`, `inertia` (weights).
    - Outputs: Returns gbest (best state found) and h (minimum fitness found).

6. **main**: It handles user input and runs the pso function.
    - Inputs Takes input from user for n_sub, n_parts, r_maxv, n_iter and n_samp.
    - Outputs: Prints the best state found and its fitness score.

## Usage
Run the script in a Python environment.
When prompted, input the following parameters: n_sub, n_parts, r_maxv, n_iter and n_samp.
The script will output the best state found and its fitness score.
For multiple trials, the script will also output an average h-score.

## License
This project is licensed under the MIT License.
