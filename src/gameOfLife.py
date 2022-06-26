import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from enums import InitialState
from utils import closeToBoundary, getLiveNN, phi_linear, setUpBlinkers, setUpGlider, setUpGliders

matplotlib.use('TKAgg')

def chooseInitialCondition():
    print("Possible initial conditions: ")
    print("* Random (1) \n* Blinker (2) \n* Glider (3)")
    initState = int(input(f"Choose initial condition: "))
    if initState not in range(1,4):
        raise ValueError("Selected choice not available. Try again.")
    return InitialState(initState)

class GameOfLife:
    def __init__(self, initCondition=0, l=0, nstep=3000, seed=14122000):
        self.l = l if l else int(input("Length of lattice: "))
        self.nstep = nstep
        self.rng = np.random.default_rng(seed)
        if initCondition > 0 and initCondition < 4:
            self.initState = InitialState(initCondition)
        else:
            self.initState = chooseInitialCondition()
        self.array = self.obtainInitialArray()

    def obtainInitialArray(self):
        if self.initState == InitialState.RANDOM:
            return self.rng.choice(2, size=(self.l, self.l))
        elif self.initState == InitialState.BLINKER:
            return setUpBlinkers(self.l)
        else:
            # initState is InitialState.GLIDER
            # Uncomment for one glider or leave it for several
            # return setUpGlider(self.l)
            return setUpGliders(self.l)

    def updateCells(self):
        temporaryArray = np.copy(self.array)
        for row in range(self.l):
            for col in range(self.l):
                cell = temporaryArray[row, col]
                liveNN = getLiveNN(temporaryArray, self.l, row, col)
                # if cell is alive (cell == 1)
                if cell:
                    if liveNN < 2 or liveNN > 3:
                        # any live cell with less than 2 live nn dies
                        # any live cell with more than 3 live nn dies
                        self.array[row, col] = 0
                # else, cell is dead, cell == 0
                else:
                    if liveNN == 3:
                        # any dead cell with 3 live nn becomes alive
                        self.array[row, col] = 1

    def updateCells_fast(self):
        """Faster method to update cells; thanks to the use of np.roll and bool masking"""
        # nn for left - right - up -down
        live_nn = np.roll(self.array, 1, axis=0) + np.roll(self.array, 1, axis=1) + \
            np.roll(self.array, -1, axis=0) + np.roll(self.array, -1, axis=1) + \
            np.roll(self.array, (1, 1), axis=(0, 1)) + np.roll(self.array, (-1, 1), axis=(0, 1)) + \
            np.roll(self.array, (1, -1), axis=(0, 1)) + np.roll(self.array, (-1, -1), axis=(0, 1))   

        mask = (live_nn > 3) | (live_nn < 2)
        make_dead = mask * self.array
        make_alive = ((live_nn == 3) * ~self.array.astype(bool)) * 1
        new_arr = np.where(make_dead, 0, self.array)
        new_arr = np.where(make_alive, 1, new_arr)
        self.array = new_arr

    def animate(self):
        # fig, ax = plt.subplots(figsize=(8,8))
        # fig.suptitle('Game of Life', fontsize=16)
        plt.imshow(self.array, animated=True, vmin=0, vmax=1)
        aliveCells = []
        for epoch in range(self.nstep):
            print(f"Epoch number {epoch}")
            aliveCells.append(np.sum(self.array))
            self.updateCells_fast()
            plt.cla()
            plt.imshow(self.array, animated=True, vmin=0, vmax=1)
            plt.draw()
            plt.pause(0.0001)

    def getEquilibriumTime(self):
        aliveCells = []
        counterAliveCells = 0
        equilibriumTime = 0
        for epoch in range(self.nstep):
            aliveCells.append(np.sum(self.array))
            self.updateCells_fast()
            if aliveCells[-1] == np.sum(self.array):
                if counterAliveCells == 0:
                    equilibriumTime = epoch
                counterAliveCells += 1
                if counterAliveCells == 10:
                    break
            else:
                equilibriumTime = 0
                counterAliveCells = 0
        return equilibriumTime

    def getCoMData(self, nstep=30):
        if self.initState != InitialState(3):
            raise ValueError("Initial state should be the Glider. Try again")
        xs, ys = [], []
        for step in range(nstep):
            self.updateCells()
            if not closeToBoundary(self.array, self.l):
                com = self.getCoM(self.array)
                xs.append(com[0])
                ys.append(com[1])

        xs = np.array(xs)[:,None]
        ys = np.array(ys)[:,None]
        times = np.array(list(range(1, len(xs)+1)))[:,None]
        sns.set_theme()
        _, axs = plt.subplots(1, 2, figsize=(14, 8))
        sns.set_theme()

        axs[0].plot(times, xs, label='xs com')
        axs[0].scatter(times, xs, label='xs com scatter')

        w_fit = np.linalg.lstsq(phi_linear(times), xs, rcond=None)[0]
        print(w_fit)
        X_grid = np.arange(0, nstep, 0.01)[:,None]
        f_grid = np.dot(phi_linear(X_grid), w_fit)
        axs[0].plot(X_grid, f_grid, label='linear regression fit')

        axs[0].set_xlabel('Time')
        axs[0].set_ylabel('x-coordinate')
        # plt.legend()
        # plt.show()

        # fig2 = plt.figure(figsize=(10,8))

        axs[1].plot(times, ys, label='ys com')
        axs[1].scatter(times, ys, label='ys com scatter')

        w_fit = np.linalg.lstsq(phi_linear(times), ys, rcond=None)[0]
        print(w_fit)

        f_grid = np.dot(phi_linear(X_grid), w_fit)
        axs[1].plot(X_grid, f_grid, label='linear regression fit')

        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('y-coordinate')
        plt.legend()
        plt.show()

    def getCoM(self, arr):
        idxs = np.asarray(np.where(arr == 1)).T
        return np.mean(idxs, axis=0)

