# phase_array
### Hi! :blush: Welcome to the n_queens README.md! 😲 
This repository represents an attempt at general solution to optimal arrangement of nodes in a hypothetical phase array.
We reduce this problem (a lot) to a famous, easy-to-grasp and NP-hard search problem NQueens. 
We attempt this problem with a few different optimization metaheuristics:
  - Genetic Algorithm
  - Particle Swarm Optimization
  - Simulated Annealing
  - Steepest Ascent with Random Restart
  - Quantum Annealing

We then rate the performance of each implementation, where a high performance is denoted by a low number of calls to the fitness function and strong tendency towards the optimal state as N tends to the highest known solution for NQueens, 27. Following are explanations for the usage and understanding of each algorithm. 

# Genetic Algorithm Approach :dna:

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

# Particle Swarm Optimization Approach 🐝 
## Description
This script uses the Particle Swarm Optimization (PSO) algorithm to solve the N-Queens problem. The goal of this script is to provide an optimized solution for the problem using PSO.

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
    - Inputs Takes input from user for `n_sub`, `n_parts`, `r_maxv`, `n_iter` and `n_samp`.
    - Outputs: Prints the best state found and its fitness score.

## Usage
Run the script in a Python environment.
When prompted, input the following parameters: `n_sub`, `n_parts`, `r_maxv`, `n_iter` and `n_samp`.
The script will output the best state found and its fitness score.
For multiple trials, the script will also output an average h-score.

## License
This project is licensed under the MIT License.

# Steepest Ascent with Random Restart Approach 🗻

## Description
This script implements a Steepest Ascent Hill Climbing algorithm with Random Restart to solve the N-Queens problem. 

## How it Works
The script works by exploring the problem space for the best neighbor state using a Steepest Ascent approach. If it reaches a peak where no better neighboring states can be found, it performs a random restart and begins the search again. The algorithm continues until the maximum number of iterations is reached or a solution is found.

The algorithm employs a heuristic cost function, h(state), which calculates the total number of conflicts in a given state. The fewer the conflicts, the better the state.

## Code Structure
The main function `steepestAscentRandomRestart` manages the random restarts and calls the `steepestAscent` function each time a restart is done. The `steepestAscent` function performs the Steepest Ascent Hill Climbing search.

Auxiliary functions include `repeatSARR` which repeats the Steepest Ascent with Random Restart process multiple times to obtain average results.

## Inputs and Outputs
1. **steepestAscent**: The main steepest ascent algorithm.
    - Input: `state`, `convInfo`, `idx`, `totalItr`, `minh`.
    - Output: `current`, `h`, `count`, `convInfo`, `idx`, `totalItr`, `minh`.

2. **steepestAscentRandomRestart**: Function implementing random restarts.
    - Input: `maxItr`, `state`, `numRuns`, `numRestarts`.
    - Output: `estimateRestarts`, `estimateSteps`, `convInfo`, `idx`.

3. **repeatSARR**: Average results from multiple runs of the algorithm.
    - Input: `numLoops`, `state`, `numRuns`, `numRestarts`.
    - Output: `convInfo`.

## Execution
To run the algorithm, call the `repeatSARR` function with appropriate parameters. You can specify the maximum number of iterations (`maxItr`), the number of loops to average over (`numLoops`), and the number of runs and restarts per loop (`numRuns`, `numRestarts`).

## License
This project is licensed under the MIT License.

# Simulated Annealing Approach 🥇

## Description
This script implements a Simulated Annealing algorithm to solve the N-Queens problem. 

Simulated Annealing is a probabilistic technique for approximating the global optimum of a given function. It's a metaheuristic to approximate global optimization in a large search space. It is often used when the search space is discrete. 

This specific implementation includes an optional quantum tunneling feature that helps the search jump out of local minimums and explore other areas of the search space.

## How it Works
The script works by exploring the problem space for a better state using a Simulated Annealing approach. This means that it probabilistically decides whether to move to a new state based on the difference in heuristic cost and the current 'temperature' (a metaphorical control parameter that decreases over iterations).

The quantum tunneling feature is added to encourage more exploration. With a set probability, the algorithm makes a significant jump in the problem space instead of a small local move. This feature can be useful when the problem space has many local minima.

The algorithm employs a heuristic cost function, h(state), which calculates the total number of conflicts in a given state. The fewer the conflicts, the better the state.

## Code Structure
The main function `simulatedAnnealing` performs the Simulated Annealing search, while the function `repeatSIM` calls the `simulatedAnnealing` function multiple times to obtain average results.

## Inputs and Outputs
1. **simulatedAnnealing**: The main Simulated Annealing algorithm.
    - Input: `maxItr`, `state`, `numRuns`, `tunnelingProb`.
    - Output: `convInfo`.

2. **repeatSIM**: Average results from multiple runs of the algorithm.
    - Input: `maxItr`, `numLoops`, `state`, `numRuns`, `tunnelingProb`.
    - Output: `convInfo`.

## Execution
To run the algorithm, call the `repeatSIM` function with appropriate parameters. You can specify the maximum number of iterations (`maxItr`), the number of loops to average over (`numLoops`), and the number of runs (`numRuns`). The `tunnelingProb` parameter sets the probability of performing a quantum tunneling operation.

## License
This project is licensed under the MIT License.

# Meta-comparison of N-Queens Heuristic Approaches 💗

## Description
This script performs a comparison of several heuristic approaches for solving the N-Queens problem. It imports the following heuristic modules: Steepest Ascent Hill Climbing with Random Restart (SARR), Simulated Annealing (SIM), Quantum Simulated Annealing (QSIM), Genetic Algorithm (GA), Genetic Algorithm variant (GAv2), and Particle Swarm Optimization (PSO). It visualizes the results of these algorithms by plotting the minimum conflicts against the number of objective function calls for each algorithm, facilitating a side-by-side comparison.

## How it Works
The script generates a random initial state and runs each of the imported modules with this initial state. It averages the results from multiple runs of each algorithm and stores the convergence information (minimum conflicts and number of objective function calls) in separate variables for each algorithm.

It then plots the convergence information for each algorithm on a single graph, with the x-axis representing the number of objective function calls and the y-axis representing the minimum number of conflicts.

## Code Structure
The main function, `main`, handles the creation of the initial state, the running of the modules, and the creation of the plot.

## Inputs and Outputs
**main**: The main function that runs everything.
- Input: None (parameters are hardcoded)
- Output: None (results are displayed in a plot)

## Execution
To run the script, simply execute the script in a Python environment. It will run each of the imported modules with the specified parameters, average the results, and display a plot of the results. 

## Notes
Before running the script, make sure all the mentioned modules (n_queens_SARR, n_queens_SIM, n_queens_GA, n_queens_GAv2, and n_queens_PSO) are in the same directory as the script and that all required packages are installed.

## License
This project is licensed under the MIT License.

