Genetic Algorithm for Phased Array Calibration
In the near future we want to use a genetic algorithm to maximize output parameters of a phased array for synthetic aperture radar (SAR) applications. We want to maximize an unknown function of 64 continuous variables, one for each element of an 8x8 array. For example we could want to maximize the amplitude of the transmitted signal using the optimal combination of 64 array element values. To do this we can start with the simplified discrete version of the problem (N=8 Queens) and adapt it to the continuous version (64 element phased array).
Proposed steps:

●	Download Q5 problem folder, EECS 492 pdf, and book
●	Attempt problem 5.3 from HW 1 from EECS 492 Foundations of AI
○	Read sections 4 (pg 233) to 4.1.4 (pg 250) from AI A Modern Approach
○	Download IDE, Python, and necessary packages (numpy, random)
○	Successfully run Q5\main.py
○	Implement the genetic algorithm function in Q5\utils.py according to problem definition
○	Compare to solution
●	Research continuous genetic algorithm implementations, make appropriate changes to data structures/paring/mating/mutations, and verify convergence with a simple objective function of 64 variables
●	Implement genetic algorithm with phased array measurement feedback loop 
