# Hi! :blush: Welcome to the phase_array README.md! 😍 We hope this helps! 😝
## Phase Array Calibrator 📡

This Python repository focuses on creating a phase array calibrator that optimizes the amplitude of a beamformer by adjusting the positions of AWS-0103 modules and attenuators. The calibrator accepts binary files representing the board state of a phased array's phase shifters and alters their values to calibrate the beamformer in a user-defined configuration.

## Problem Statement 📓

Given the complex and multidimensional nature of our problem, we don't have a well-defined function relating the beamformer wave magnitude to the phase shifter and attenuator values. As a result, we use metaheuristic algorithms to search the solution space for an optimal solution efficiently. 

To evaluate the performance of these metaheuristic algorithms, we demonstrate their effectiveness on the classic NP-hard NQueens problem because of its multidimensional and computationally heavy nature. We use several different metaheuristics (Particle Swarm Optimization (PSO), Genetic Algorithm (GA), Simulated Annealing, Steepest Ascent Random Restart, and Quantum Annealing) and rate them based on their calls to the fitness function and convergence to the optimal solution.

## Solution Approach 

The main bottleneck in our problem is the calls to the fitness function because each call requires us to loop through the entire system: from the beamformer to grab the state, through the Software Defined Radio (SDR) to digitize the signal, and then back to the Python program to rate its efficacy. 

The bin folder contains our work on a closer representation of the real problem. Here, we take a 16x16 string of 6-bit integers and optimize it to the optimal state, which is a randomly generated 16x16 string of 6-bit integers.

## Project Structure 📁

- `n_queens/` - Contains the implementation and tests for metaheuristic algorithms on the NQueens problem.
- `bin/` - Contains tests of the best-performing algorithms from `n_queens/` on a more representative problem.

## Usage 

- To run the NQueens problem, navigate to the `n_queens/` directory and run the Python script corresponding to the algorithm you want to test.
- To test the algorithms on the representative problem, navigate to the `bin/` directory and run the Python script corresponding to the algorithm you want to test.

## Dependencies 🤘

- Python 3.x
- NumPy
- matplotlib

## Contribution ⛑️

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/cawley/phase_array/issues) if you want to contribute.

## Authors ✏️

- [Liam Cawley](https://github.com/cawley)
- [Gabe Ronan](https://github.com/ronangabriel)

## License 🚙

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.
