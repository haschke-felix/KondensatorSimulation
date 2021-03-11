import numpy as np
import simulation as sim
import fieldplot as fplot
import roundPlateCapacitor as roundCap
import easygui
import matplotlib.pyplot as plt
import sys

path = "/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_0.01/cap.npy"
resolution = 200
width = 1.0
try:
    resolution = int(sys.argv[1])
except:
    pass
try:
    width = sys.argv[2]
except:
    pass
try:
    path = sys.argv[3]
except:
    pass

def distributionAnalysis(charges,n=512, rad=2, dist=1, tol=0.1):
    # generate grid
    print("generating grid")
    r = np.linspace(0, rad, n)
    x_1 = np.linspace(0, rad, n)
    print(r.shape, x_1.shape)

    grid_1, grid_2 = np.meshgrid(r, x_1)
    grid = np.array((grid_1,grid_2,np.zeros(grid_1.shape)))

    charges = charges.swapaxes(0,1)
    con = np.subtract(grid[:,:,:,None], charges[:,None,None,:])
    E = con / (charges[0, :] * (np.linalg.norm(con,axis=0)**3))
    E = np.sum(E,axis=3)

    E = np.linalg.norm(E, axis=0)

    cap_sum = 0
    sum = 0

    for b_ in range(0, n):
        print(b_)
        if np.abs(dist - x_1[b_]) > tol:
            continue
        for r_ in range(0, n):
            sum += E[b_][r_]
            if r[r_] < 1:
                cap_sum += E[b_][r_]
                
    print("total: ", sum)
    print("in capacitor", cap_sum)
    print("quotient", cap_sum / sum)
    return sum, cap_sum

def chunked(cap,n=resolution,rad=50, tol=0.01, dist=width, chunkxy=2):
    xy = np.linspace(0,chunkxy, chunkxy)
    xy * rad
    print(xy)
    #distributionAnalysis(cap,n=resolution,rad=50, tol=0.01, dist=width)



cap = sim.load(path)

#chunked(cap)
distributionAnalysis(cap,n=resolution,rad=40, tol=0.01, dist=width)

    

def oneAxisDistribution():
    space = np.linspace(-10,10, 10000)
    spaceGrid = np.array([space, np.zeros(space.shape), np.zeros(space.shape)])
    
    charges = cap.swapaxes(0,1)
    
    print("spaceGrid", spaceGrid.shape)
    con = np.subtract(spaceGrid[:,:,None], charges[:,None,:])
    print("con", con.shape)
    E = con / (charges[0, :] * (np.linalg.norm(con,axis=0)**3))
    E = np.sum(E,axis=2)
    print("E", E.shape)
    normE = np.linalg.norm(E, axis=0)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(space, normE, '-')
    
    plt.show()