import numpy as np
import simulation as sim
import fieldplot as fplot
import roundPlateCapacitor as roundCap
import easygui
import matplotlib.pyplot as plt
import sys

path = "/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_1.0/cap.npy"
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

def distributionAnalysis(charges,n=200, radr0=0, radb0=0, rad=2, dist=1, tol=0.1):
    print("params", n, radr0, radb0, rad, dist, tol)
    # generate grid
    print("generating grid")
    r = np.linspace(radr0, radr0 + rad, n)
    x_1 = np.linspace(radb0, radb0 + rad, n)
    print(r.shape, x_1.shape)

    grid_1, grid_2 = np.meshgrid(r, x_1)
    grid = np.array((grid_1,grid_2,np.zeros(grid_1.shape)))

    charges = charges.swapaxes(0,1)
    con = np.subtract(grid[:,:,:,None], charges[:,None,None,:])
    E = con / (charges[0, :] * (np.linalg.norm(con,axis=0)**3))
    E = np.sum(E,axis=3)

    E = np.linalg.norm(E, axis=0)
    
    E = E * r[None,:]

    cap_sum = 0
    sum = 0

    for b_ in range(0, n):
        #print(b_)
        if np.abs(dist - x_1[b_]) < tol:
            continue
        for r_ in range(0, n):
            #print("j", r_)
            sum += E[b_][r_]
            if r[r_] < 1:
                cap_sum += E[b_][r_]
                
    print("total: ", sum)
    print("in capacitor", cap_sum)
    print("quotient", cap_sum / sum)
    return sum, cap_sum

def chunked(cap,chunksize,rad=50, tol=0.1, dist=width, chunks=2):
    sumcap = 0
    sum = 0
    partial_rad = rad/chunks
    for i in range(0, chunks):
        for j in range(0, chunks):
            print("ij", (i,j))
            s,cs = distributionAnalysis(cap, n=chunksize, radr0=i*partial_rad, 
            radb0=j*partial_rad, rad=partial_rad, tol=tol, dist=width)
            sumcap += cs
            sum += s
    print("total: ", sum)
    print("in capacitor", sumcap)
    print("quotient", sumcap / sum)
    return sum, sumcap



cap = sim.load(path)
resolution = 100
chunked(cap,chunksize=resolution,rad=50, tol=0.01, dist=width, chunks = 8)
#distributionAnalysis(cap,n=resolution,rad=10, tol=0.1, dist=width)

    

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