import numpy as np
import simulation as sim
import fieldplot as fplot
import roundPlateCapacitor as roundCap
import easygui
import matplotlib.pyplot as plt

width = 0.4

path = "/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_{}/cap.npy".format(width)
cap = sim.load(path)

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
limit = width - tol
grid = np.linspace(-limit, limit, resolution)

# normale Kondensatorformel
opt_E = len(cap)/(4*8.85*10**-8) / 2
opt_W = opt_E * width
print("optw", opt_W) 

x_2_pos = np.linspace(0,2,40)
works = []
for x_2_p in x_2_pos:
    E = oneAxisField(grid, cap, width, x_2 = x_2_p)
    work = E.sum(axis=1) * width / resolution
    workabs = np.linalg.norm(work)
    print("sum E-Norm x_2 = {}:".format(x_2_p), workabs)
    works.append(workabs)

avg = np.average(np.array(works))
for i in range(len(works)):
    print("work percent avg {}".format(x_2_pos[i]), works[i] / avg)

w = .8 * np.max(x_2_pos) / len(x_2_pos)
ax.plot(x_2_pos, np.array(works) / opt_W, '.')
# print opt
ax.plot(x_2_pos, np.full(x_2_pos.shape, 1), '--', color='black',label='Optimaler Kondensator')

#ax.plot(grid, np.full(grid.shape, 1), '--', color='black', label='Optimaler Kondensator')
#ax.set_xlabel('$x_1$')
#ax.set_ylabel('Anteil der "optimalen" Feldstärke (%)')
ax.set_ylim(0,1.1)
plt.legend()
plt.show()
