import numpy as np
import simulation as sim
import fieldplot as fplot
import roundPlateCapacitor as roundCap
import easygui
import matplotlib.pyplot as plt

widths = [0.12, 0.2, 0.5, 1.0]
caps = []
colors = [('-', 'green'),('-', 'red'),('-', 'blue'),('-', 'orange')]

for w in widths:
    path = "/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_{}/cap.npy".format(w)
    caps.append(sim.load(path))
def oneAxisField(grid, cap, dist=1):
    spaceGrid = np.array([grid, np.zeros(grid.shape), np.zeros(grid.shape)])
    
    charges = cap.swapaxes(0,1)
    
    con = np.subtract(spaceGrid[:,:,None], charges[:,None,:])
    E = con / (charges[0, :] * (np.linalg.norm(con,axis=0)**3))
    E *= dist # Ladung ausgleichen
    E /= 4*np.pi*(8.85*10**-8)
    E = np.sum(E,axis=2)
    return E

fig = plt.figure()
ax = fig.add_subplot(111)

limit = 4
grid = np.linspace(-limit, limit, 1000)

# normale Kondensatorformel
opt_E = len(caps[0])/(4*8.85*10**-8) / 2

for i in range(len(caps)):
    print(i)
    E = oneAxisField(grid, caps[i], widths[i])
    #shape, color = colors[i]
    ax.plot(grid, -E[0] / opt_E , '-',label="Abstand: {}".format(widths[i]*2))
    


ax.plot(grid, np.full(grid.shape, 1), '--', color='black', label='Optimaler Kondensator')
ax.set_xlabel('$x_1$')
ax.set_ylabel('Anteil der "optimalen" Feldstärke (%)')
plt.legend()
plt.show()
