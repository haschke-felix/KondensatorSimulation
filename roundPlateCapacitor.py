import multiprocessing as mp
import psutil
import numpy as np
from enum import Enum
import time
import simulation as sim
import os

R = 1

def simulateThreaded(cap,steps, step=0.4, dist=1, savepath="", saveInterval=100):
    path = savepath + "/round-{}-step:{}-dist:{}".format(len(cap), step, dist)
    os.mkdir(path)
    count = 0
    for i in range(0,steps):
        simStepThreaded(cap, step)
        print("iteration: ", i, end=" ")
        if (len(savepath) > 0) and (i % saveInterval == 0):
            sim.save(cap, path=(path + "/steps/$cap-{}.npy".format(i)))
    if len(savepath) > 0:
        sim.save(cap, path=(path + "/cap.npy"))

    return cap


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
        tmpE *= 100
        tmpE[0] = 0 # necessary in order keep charges on plate 

        # check minimum move distance
        min_dist = np.amin(np.ma.masked_equal(distances, 0))
        self.min_factor = min(self.min_factor, self.step * min_dist / np.linalg.norm(tmpE))
        
        # determine temporary position (if force vector is just applied)
        tmp_pos = np.add(charge, self.min_factor * tmpE)

        if _surfaceOption(tmp_pos) == _SurfaceState.Outside:
            pre_opt = _surfaceOption(charge)
            # if currently considered point is outside range, additional steps have to be performed
            if pre_opt == _SurfaceState.OnSurface:
                # only move upon outline has been reached --> figure out intersection
                # abs{p + a * F} = r <=>  0 = a^2(F[1]^2+F[2]^2) + a(p[1]*[E[1] + p[2]*E[2]) + p[1]^2 + p[2]^2- r^2 )
                # solve this polynom using pq-formula function:
                tmpE = mapToOutline(charge, tmpE)
    
                # updating min factor
                #self.min_factor = min(self.min_factor, np.linalg.norm(tmpE))
            
            if pre_opt == _SurfaceState.OnOutline:
                # figure out the angle between E and the charge position

                # The field vector points somewhere between the both sides of the tangent:
                dot_product = np.dot(charge[1:3], tmpE[1:3])
                if dot_product > 0:
                    E_parallel = tmpE[1:3] - charge[1:3] * dot_product / (np.linalg.norm(charge[1:3]))
                    target_pos = tmpE[1:3] / np.linalg.norm(tmpE[1:3]) * R

                    tmpE[1:3] = target_pos
                    # not considering min_factor at this point

                # The field vector intersects with the circle again (opposite side)
                else:
                    # unlikely case... 
                    # minimize min factor in the way, that the position cant reach out of the plate
                    tmp = mapToOutline(charge, tmpE)
                    max_dist = np.linalg.norm((charge-tmp)[1:3])
                    real_dist = np.linalg.norm(tmpE[1:3])
                    print("encountered force putting the charge from outside through the circle outside!")
                    #self.min_factor = min (self.min_factor, max_dist / real_dist)
        return tmpE

def mapToOutline(p, E):
    # abs{p + a * E} = r <=>  0 = a^2(E[1]^2+E[2]^2) + a(p[1]*[E[1] + p[2]*E[2]) + p[1]^2 + p[2]^2- r^2 )
    # solve this polynom using pq-formula function:
    len_fact = solvePoly2(E[1]**2 + E[2]**2, p[1]*E[1] + p[2]*E[2], p[1]**2 + p[2]**2 - R**2)
    return E * len_fact            

def simStepThreaded(charges, step=0.4):
    procs = list()
    n_cpus = (psutil.cpu_count() * 5) // 4
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
    E *= min_factor 
    E += charges
    for i in range (len(charges)):
        charges[i] = _validate(charges[i],E[i])
    #return np.apply_along_axis(_validate ,1,charges + E * min_factor)

## collision handling
class _SurfaceState(Enum):
    OnSurface = 1
    OnOutline = 2
    Outside = 3

def _surfaceOption(pos):
    # determine whether the position is inside the circle or not
    r= np.hypot(pos[1],pos[2])
    if r > R:
        return _SurfaceState.Outside
    if np.isclose(r,R):
        return _SurfaceState.OnOutline
    return _SurfaceState.OnSurface

def _validate (pos, new_pos):
    # store the charge
    charge = new_pos[0]
    #outside
    
    hyp = np.hypot(new_pos[1], new_pos[2])
    if np.hypot(new_pos[1], new_pos[2]) > R and not np.isclose(hyp,R):
        print("A position outside the circle has been encountered, This case should not occur")
        print(np.hypot(new_pos[1], new_pos[2]),pos,new_pos)
        new_pos /= np.linalg.norm(new_pos[1:3]) * R
    
    # special case: if the charge already was on the outline
    # then set to outline also if currently not on outline
    if _surfaceOption(pos) == _SurfaceState.OnOutline:
        new_pos /= np.linalg.norm(new_pos[1:3]) * R
    
    new_pos[0] = charge

    return new_pos

def solvePoly2(a, b, c):
    # applying pq formula:
    # only positive solution needed for
    p_ = b/(2*a)
    q = c/a
    solution = - p_ + np.sqrt( p_*p_ - q)
    return solution


def setupCapacitor(step=0.2, dist=1):
    # marking rings with the specified distance
    # on these rings, try to make a distance of the distance
    circle_radius = np.arange(start=step, stop=R,step=step)
    circle_num = np.rint(circle_radius * (2 * np.pi / step))
    total_num = int(circle_num.sum())
    print("In total, {} charges per plate are going to be generated".format(total_num))

    charges_plus = np.zeros((total_num, 3))
    charges_minus = np.zeros((total_num, 3))

    i = 0
    for r, n in zip(circle_radius, circle_num):
        perimeter = np.pi * 2 * r
        # generate single charges
        for _ in range(int(n)):
            alpha = 2 * np.pi * i / n
            charges_plus[i] = np.array((dist, r*np.sin(alpha), r*np.cos(alpha)))
            charges_minus[i] = np.array((-dist, r*np.sin(alpha), r*np.cos(alpha)))
            i += 1
    return np.concatenate((charges_plus, charges_minus))

def setupCapacitorAllChargesOnOutline(step=0.2):
    # placing the charges on the outer ring only

    total_num = 360
    charges_plus = np.zeros((total_num, 3))
    charges_minus = np.zeros((total_num, 3))

    i = 0
    # generate single charges
    for _ in range(int(total_num)):
        alpha = 2 * np.pi * i / total_num
        charges_plus[i] = np.array((1, R*np.sin(alpha), R*np.cos(alpha)))
        charges_minus[i] = np.array((-1, R*np.sin(alpha), R*np.cos(alpha)))
        i += 1
    return np.concatenate((charges_plus, charges_minus))