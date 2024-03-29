import multiprocessing as mp
import psutil
import numpy as np
from enum import Enum
import time
import simulation as sim



class SimCore(object):
    def __init__(self, charges, cpunum, a,b,step=0.4):
        self.min_factor = 1
        self.E = np.zeros((b-a,3))
        self.charges = charges
        self.step = step
        self.a = a
        self.b = b

    def run(self, coreNum, dict):
        for n in range(self.a,self.b):
            self.E[n-self.a] = self._processSingleCharge(n)
        dict[coreNum] = (coreNum, self.min_factor, self.E)
 
    def _processSingleCharge(self, i):
                # evaluate single field
        charge = self.charges[i]
        connections = np.subtract(charge,self.charges)
        distances = np.linalg.norm(connections,axis=1)

        distances[i] = 1 # avoid division by zero
        tmpE = charge[0] * (connections / (self.charges.swapaxes(0,1)[0] * (distances**3))[:,np.newaxis]).sum(axis=0)
        tmpE[0] = 0 # necessary in order keep charges on plate 

        min_dist = np.amin(np.ma.masked_equal(distances, 0))
                
        self.min_factor = min(self.min_factor, self.step * min_dist / np.linalg.norm(tmpE))
        tmp_pos = np.add(charge, self.min_factor * tmpE)

        # if currently considered point is outside range, additional steps have to be performed
        if _surfaceOption(tmp_pos) == _SurfaceState.Outside:
            opt = _surfaceOption(charge)
            if opt == _SurfaceState.OnOutline:
                # only consider the tangential field
                if np.isclose(abs(charge[1]),1):
                    tmpE[1] = 0
                if np.isclose(abs(charge[2]),1):
                    tmpE[2] = 0
            if opt == _SurfaceState.OnSurface:
                # only move till on Outline --> figure out intersection
                # handle x / [1] component
                border = (1 if tmpE[1] > 0 else -1) - charge[1]
                len_y = np.linalg.norm((border * tmpE[1] / tmpE[2],border))
                # handle y / [2] component
                border = (1 if tmpE[2] > 0 else -1) - charge[2]
                len_x = np.linalg.norm((border * tmpE[2] / tmpE[1], border))
                self.min_factor = min(self.min_factor, min(len_x, len_y) / np.linalg.norm(tmpE))
        return tmpE


def simStepThreaded(charges, step=0.4):
    procs = list()
    n_cpus = (psutil.cpu_count() * 4) // 5
    n = len(charges)
    n_step = n // n_cpus

    ranges = []
    manager = mp.Manager()
    result_dict = manager.dict()
    
    for i in range(n_cpus-1):
        ranges.append ((i, n - n_step , n))
        n -= n_step
    ranges.append ((n_cpus-1,0,n))


    jobs = []
    for cpu_range in ranges:
        core = SimCore(charges, *cpu_range, step=step)
        jobs.append(core)
        p = mp.Process(target=core.run, args=(cpu_range[0],result_dict))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    

    
    E = np.empty((0,3))
    min_factor = 1
    resList = result_dict.values()
    resList.sort(key=lambda x: x[0])

    for coreNum, fact, Ep in resList:
        E = np.concatenate((Ep,E))
        min_factor = min (min_factor, fact)

    print("min_factor:", min_factor)

    # move the charges according to the outfigured vectors
    return np.apply_along_axis(_validate ,1,charges + E * min_factor)
    

## collision handling
class _SurfaceState(Enum):
    OnSurface = 1
    OnOutline = 2
    Outside = 3

def _surfaceOption(pos):
    if(abs(pos[0]) > 1 or abs(pos[1]) > 1):
        return _SurfaceState.Outside
    if(np.isclose(abs(pos[0]),1) or np.isclose(abs(pos[1]),1)):
        return _SurfaceState.OnOutline
    return _SurfaceState.OnSurface

def _validate (pos):
    if (not np.isclose(abs(pos[1]),1)) and abs(pos[1]) > 1:
        pos[1] = -1 if pos[1] < 0 else 1
    if (not np.isclose(abs(pos[2]),1)) and abs(pos[2]) > 1:
        pos[2] = -1 if pos[2] < 0 else 1
    return pos
