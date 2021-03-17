import numpy as np
import simulation as sim
import fieldplot as fplot
import roundPlateCapacitor as roundCap
import easygui
import matplotlib.pyplot as plt

widths = [0.1, 0.2, 0.5, 1.0]
caps = []

for w in widths:
    path = "/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_{}/cap.npy".format(w)
    caps.append(sim.load(path))


def oneAxisField(grid, cap, dist=1, x_2=0):
    spaceGrid = np.array([grid, np.full(grid.shape, x_2), np.zeros(grid.shape)])
    
    charges = cap.swapaxes(0,1)
    
    con = np.subtract(spaceGrid[:,:,None], charges[:,None,:])
    E = con / (charges[0, :] * (np.linalg.norm(con,axis=0)**3))
    E *= dist # Ladung ausgleichen
    E /= 4*np.pi*(8.85*10**-8)
    E = np.sum(E,axis=2)
    return E

fig = plt.figure()
ax = fig.add_subplot(111)

tol = 0.05
resolution = 1000

# radius
x_2_pos = np.linspace(0,1,100)

# normale Kondensatorformel
opt_E = len(caps[0])/(4*8.85*10**-8) / 2

# print opt
ax.plot(x_2_pos, np.full(x_2_pos.shape, 100), '--', color='black',label='Idealer Kondensator')


def workSingleCap(cap, width):
    limit = width - tol
    grid = np.linspace(-limit, limit, resolution)
    works = []
    
    for x_2_p in x_2_pos:
        E = oneAxisField(grid, cap, width, x_2 = x_2_p)
        work = E.sum(axis=1) * width * 2 / resolution
        workabs = np.linalg.norm(work)
        print("sum E-Norm x_2 = {}:".format(x_2_p), workabs)
        works.append(workabs)
    
    avg = np.average(np.array(works))
    for i in range(len(works)):
        print("work percent avg {}".format(x_2_pos[i]), works[i] / avg)
    
    opt_W = opt_E * width * 2
    w = .8 * np.max(x_2_pos) / len(x_2_pos)
    ax.plot(x_2_pos, 100*np.array(works) / opt_W, '-', label="Breite: {}".format(width*2))

for i in range(len(widths)):
    workSingleCap(caps[i], widths[i])


#ax.plot(grid, np.full(grid.shape, 1), '--', color='black', label='Optimaler Kondensator')
ax.set_xlabel('Radius $r$')
ax.set_ylabel('Anteil der "idealen" Spannung (%)')
ax.set_ylim(0, 110)
plt.legend()
plt.show()
