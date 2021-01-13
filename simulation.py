import sys
import numpy as np
from enum import Enum
from scipy.spatial import distance_matrix

def setupCapacitor(n):
    cy = np.linspace(-1, 1,num=n,endpoint=True)
    cz = np.linspace(-1, 1,num=n,endpoint=True)
    Cy, Cz = np.meshgrid(cy, cz)
    plateplus = np.array((np.full((n,n),1),Cy,Cz))
    plateminus = np.array((np.full((n,n),-1),Cy,Cz))
    return np.concatenate((plateplus,plateminus),axis=1).reshape(3,-1).swapaxes(0,1)

def save(charges, path):
    assert len(charges.shape) == 2 and charges.shape[1] == 3, "charge model"
    np.save(path, charges)

def load(path):
    charges = np.load(path)
    assert len(charges.shape) == 2 and charges.shape[1] == 3, "Invalid input file"
    return charges

def simulate(charges, steps, step=0.4):
    for i in range(0,steps):
        charges = _simulateStep(charges, step)
        print("iteration: ", i)
    return charges

def _simulateStep(charges, step):
    min_factor = 1
    E = np.zeros(charges.shape)
    for i in range(0,len(charges)):
        # evaluate single field
        charge = charges[i]
        connections = np.subtract(charge,charges)
        distances = np.linalg.norm(connections,axis=1)
        E[i] = charge[0] * np.ma.masked_invalid(connections / (charges.swapaxes(0,1)[0] * (distances**3))[:,np.newaxis]).sum(axis=0)
        E[i][0] = 0 # necessary in order keep charges on plate 
        tmpE = E[i]

        min_dist = np.amin(np.ma.masked_equal(distances, 0))
                
        min_factor = min(min_factor, step * min_dist / np.linalg.norm(tmpE))
        tmp_pos = np.add(charge, min_factor * tmpE)

        # if currently considered point is outside range, additional steps have to be performed
        if _surfaceOption(tmp_pos) == _SurfaceState.Outside:
            opt = _surfaceOption(charge)
            if opt == _SurfaceState.OnOutline:
                # only consider the tangential field
                if np.isclose(abs(charge[1]),1):
                    E[1] = 0
                if np.isclose(abs(charge[2]),1):
                    E[2] = 0
            if opt == _SurfaceState.OnSurface:
                # only move till on Outline --> figure out intersection
                # handle x / [1] component
                border = (1 if tmpE[1] > 0 else -1) - charge[1]
                len_y = np.linalg.norm((border * tmpE[1] / tmpE[2],border))
                # handle y / [2] component
                border = (1 if tmpE[2] > 0 else -1) - charge[2]
                len_x = np.linalg.norm((border * tmpE[2] / tmpE[1], border))
                min_factor = min(min_factor, min(len_x, len_y) / np.linalg.norm(tmpE))
        
    print(min_factor)
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