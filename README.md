[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# Hi! :blush: Welcome to the phase_array README.md! 😍 We hope this helps! 😝
## Phase Array Calibrator 📡

This Python repository focuses on creating a calibrator application that optimizes the amplitude of a [phased array](https://en.wikipedia.org/wiki/Phased_array#:~:text=In%20antenna%20theory%2C%20a%20phased,directions%20without%20moving%20the%20antennas) by adjusting the phase shift and attenuator positions of [Anokiwave AWS-0103](https://www.anokiwave.com/products/aws-0103/index.html) beamformers. The calibrator accepts binary files representing the system state of each AWS-0103 alters phase shifter position, gain and attenuation values to calibrate each beamformer, and consequently the phased array beam, in a user-defined configuration. These two papers provide a [simple overview](https://web2.norsonic.com/wp-content/uploads/2016/10/TN-beamformers.pdf) and a more [in-depth look](https://sci-hub.ru/10.1109/8.923310) at beamformers and how they are calibrated.

## Common Approaches

 - [Maximum likelihood beamformer](https://sci-hub.se/10.23919/EUSIPCO.2019.8902753)
   - This approach models noise as a stationary Gaussian white random process and the signal waveform as deterministic and unknown. 
- [Bartlett beamformer](https://sci-hub.se/10.4314/njt.v36i4.23)
  - The Bartlett beamformer extends conventional spectral analysis to the Directional Arrival Assessment (DAA). The angle that maximizes the spectral power is used to estimate the angle of arrival. 
- [Capon beamformer](https://apps.dtic.mil/sti/pdfs/ADA433961.pdf)
  - Also known as the minimum-variance distortionless response (MVDR) beamforming algorithm, the Capon beamformer offers better resolution than the Bartlett approach. However, it has higher complexity due to the need for full-rank matrix inversion. Recent advances in GPU computing have made real-time Capon beamforming more feasible. 
- [MUSIC beamformer](https://sci-hub.se/10.1109/IBCAST.2014.6778172)
  - The MUSIC (MUltiple SIgnal Classification) beamforming algorithm starts by decomposing the covariance matrix for both the signal and noise parts. It uses the noise sub-space of the spatial covariance matrix in the denominator of the Capon algorithm, thus known as subspace           beamformer. This approach provides better Direction of Arrival (DOA) estimation compared to the Capon beamformer. The ESPRIT algorithm can be used as an alternative approach.
- Artificial Intelligence
  - The ongoing trend in digital signal processing for DAA involves the use of Artificial Intelligence technologies.

## Problem Statement 📓

Given the complex and multidimensional nature of our problem, we don't have a well-defined function relating the beamformer wave magnitude to the phase shifter and attenuator values. As a result, we use metaheuristic algorithms to search the solution space for an optimal solution efficiently. 

To evaluate the performance of these metaheuristic algorithms, we demonstrate their effectiveness on the classic NP-hard NQueens problem because of its multidimensional and computationally heavy nature. We use several different metaheuristics (Particle Swarm Optimization (PSO), Genetic Algorithm (GA), Simulated Annealing, Steepest Ascent Random Restart, and Quantum Annealing) and rate them based on their calls to the fitness function and convergence to the optimal solution.

## Solution Approach 👩‍🔬

The main bottleneck in our problem is the calls to the fitness function because each call requires us to loop through the entire system: from the beamformer to grab the state, through the Software Defined Radio (SDR) to digitize the signal, and then back to the Python program to rate its efficacy. 

The bin folder contains our work on a closer representation of the real problem. Here, we take a 16x16 string of 6-bit integers and optimize it to the optimal state, which is a randomly generated 16x16 string of 6-bit integers.

## Project Structure 📁

- `n_queens/` - Contains the implementation and tests for metaheuristic algorithms on the NQueens problem.
- `bin/` - Contains tests of the best-performing algorithms from `n_queens/` on a more representative problem.

## Usage 😳

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
