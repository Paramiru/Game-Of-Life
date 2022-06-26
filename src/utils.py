import numpy as np
import numpy.typing as npt

def phi_linear(Xin):
    return np.hstack([Xin, np.ones((Xin.shape[0],1))])

def closeToBoundary(array, l):
        idxs = np.asarray(np.where(array == 1)).T
        if np.any(idxs == l) or np.any(idxs == 0):
            return True
        return False
        
def getLiveNN(arr: npt.ArrayLike, l: int, row: int, col: int) -> int:
   return arr[row-1, col]         + arr[(row+1) % l, col]   + \
          arr[row, col-1]         + arr[row, (col+1) % l]   + \
          arr[row-1, col-1]       + arr[row-1, (col+1) % l] + \
          arr[(row+1) % l, col-1] + arr[(row+1) % l, (col+1) % l]

def setUpBlinkers(l: int):
        arr = np.zeros((l, l))
        midpoint = l // 2 
        arr[midpoint, midpoint] = 1
        arr[midpoint+1, midpoint] = 1
        arr[midpoint-1, midpoint] = 1
        extra_dist = l // 4 

        arr[midpoint + extra_dist,     midpoint + extra_dist] = 1
        arr[midpoint + extra_dist + 1, midpoint + extra_dist] = 1
        arr[midpoint + extra_dist - 1, midpoint + extra_dist] = 1

        arr[midpoint - extra_dist,     midpoint + extra_dist] = 1
        arr[midpoint - extra_dist + 1, midpoint + extra_dist] = 1
        arr[midpoint - extra_dist - 1, midpoint + extra_dist] = 1    

        arr[midpoint + extra_dist,     midpoint - extra_dist] = 1
        arr[midpoint + extra_dist + 1, midpoint - extra_dist] = 1
        arr[midpoint + extra_dist - 1, midpoint - extra_dist] = 1

        arr[midpoint - extra_dist,     midpoint - extra_dist] = 1
        arr[midpoint - extra_dist + 1, midpoint - extra_dist] = 1
        arr[midpoint - extra_dist - 1, midpoint - extra_dist] = 1

        return arr

def setUpGlider(l: int):
        arr = np.zeros((l, l))
        midpoint = l // 2 - 1
        arr[midpoint-1, midpoint] = 1
        arr[midpoint, midpoint+1] = 1
        arr[midpoint+1, midpoint] = 1
        arr[midpoint+1, midpoint-1] = 1
        arr[midpoint+1, midpoint+1] = 1
        return arr

def setUpGliders(l: int):
        arr = np.zeros((l, l))
        midpoint = l // 2 - 1
        for buffer in [0, l//3, -l//3]:
                arr[midpoint-1 + buffer, midpoint   - buffer] = 1
                arr[midpoint   + buffer  , midpoint+1 - buffer] = 1
                arr[midpoint+1 + buffer, midpoint   - buffer] = 1
                arr[midpoint+1 + buffer, midpoint-1 - buffer] = 1
                arr[midpoint+1 + buffer, midpoint+1 - buffer] = 1
        return arr
