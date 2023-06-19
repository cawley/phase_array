# Anokiwave AWS-0103 Beamformer Calibration 

## Overview
This repository contains Python implementations of several metaheuristic search algorithms for calibrating an Anokiwave AWS-0103 beamformer. The algorithms are general-purpose search algorithms and do not include any beamforming-specific knowledge or physics.

The implemented algorithms include:
- Genetic Algorithm (GA)
- GA with multiprocessing
- GA with multiprocessing and n-tuplet breeding
- Steepest Ascent with Random Restart

Each of these algorithms is applied to a random binary string of 6-bit binary numbers, where each binary string can be modelled as a vertex on a 16x16 graph. Each vertex represents the state (gain, attenuation, phase, etc.) of a single Anokiwave AWS-0103.

**Note:** The specific beamforming algorithm used in this project is proprietary and is not included in this repository.

## How to Use
To use these scripts, clone the repository to your local machine and execute the Python script corresponding to the desired search algorithm.

## Requirements
The project is implemented in Python and requires the following packages:
- numpy
- matplotlib

## Getting Started
Here are the steps to clone and run the project:
```
git clone https://github.com/cawleyl/phase_array/bin.git
cd beamformer_calibration
python3 genetic_algorithm.py
```
Replace `genetic_algorithm.py` with the script for the algorithm you wish to run.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contact
If you have any questions, feel free to reach out at cawleyl@umich.edu.
