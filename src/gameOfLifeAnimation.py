from gameOfLife import GameOfLife
from IO import writeEquilibrationTimes
import numpy as np

def exp1():
    """Experiment for obtaining data to plot a histogram with the 
    equilibration times.
    """

    equilibrationTimes = []
    for seed in range(1000):
        print(f'Using seed {seed}')
        # random initial condition, 50x50 square lattice
        app = GameOfLife(initCondition=1, l=50, seed=seed * 69)
        equilibrationTimes.append(app.getEquilibriumTime())
    equilibrationTimes = np.array(equilibrationTimes)
    # if any equilibration time is 0 this means that the system did
    # not reach equilibrium in the nstep used for the simulation. 
    writeEquilibrationTimes(equilibrationTimes[equilibrationTimes != 0])
    
def exp2():
    app = GameOfLife()
    app.animate()

def exp3():
    app = GameOfLife(initCondition=3, l=50)
    app.getCoMData()
    
if __name__ == "__main__":
    exp3()
