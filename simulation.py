import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from enum import Enum

def E_Field(q, r0, p):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    connection = np.subtract(p,r0)
    den = np.linalg.norm(connection)**3
    return q * connection / den

# Create a multipole with nq charges of alternating sign, equally spaced
# on the unit circle.
#nq = 2**int(sys.argv[1])

charges = []


# setup capacitor
def setupCapacitor():
    global charges
    for i in np.arange(-1.0,1.0,0.1):
        for j in np.arange(-1.0,1.0,0.1):
            charges.append((-1,(-1,i,j)))
            charges.append((1,(1,i,j)))
setupCapacitor()

#charges.append((1,(1,0.5,0)))
#charges.append((-1,(1,-0.5,0)))

factor = 0.0001

class SurfaceState(Enum):
    OnSurface = 1
    OnOutline = 2
    Outside = 3

def surfaceOption(pos):
    if(abs(pos[0]) > 1 or abs(pos[1]) > 1):
        return SurfaceState.Outside
    if(abs(pos[0]) == 1 or abs(pos[1]) == 1):
        return SurfaceState.OnOutline
    return SurfaceState.OnSurface


def stretchTo(vect, l):
    return np.array(vect) * l / np.linalg.norm(vect) 

def validate (pos):
    if abs(pos[1]) > 1:
        pos[1] = -1 if pos[1] < 0 else 1
    if abs(pos[2]) > 1:
        pos[2] = -1 if pos[2] < 0 else 1
    return pos
def simulateStep():
    print("WHATEVER!!!!")
    global charges
    forces = []
    min_factor = 1
    for qp, posp in charges:
        min_dist = np.linalg.norm(np.subtract(charges[0],charges[1]))
        E = 0, 0, 0 # Ex not relevant for movement on the plate
        for q, pos in charges:
            if(posp != pos): # make sure its not the same charge
                min_dist = min(min_dist, np.linalg.norm(np.subtract(pos, posp)))
                e = E_Field(q,pos, posp) # ex is not necessary again
                E = np.add(E, e)
        E[0] = 0
        E *= qp
        min_factor = min(min_factor, 0.5 * min_dist / np.linalg.norm(E))
        tmp_pos = np.add(posp, min_factor * E)
        # if currently considered point is outside range, additional steps have to be performed
        if surfaceOption(tmp_pos) == SurfaceState.Outside:
            opt = surfaceOption(posp)
            if opt == SurfaceState.OnOutline:
                # only consider the tangential field
                if abs(posp[1]) == 1:
                    E[1] = 0
                if abs(posp[2]) == 1:
                    E[2] = 0
            if opt == SurfaceState.OnSurface:
                # only move till on Outline --> figure out intersection
                # handle x / [1] component
                border = (1 if E[1] > 0 else -1) - posp[1]
                len_y = np.linalg.norm((border * E[1] / E[2],border))
                border = (1 if E[2] > 0 else -1) - posp[2]
                len_x = np.linalg.norm((border * [2] / E[1], border))
                min_factor = min(min_factor, min(len_x, len_y) / np.linalg.norm(E))
        
        forces.append(E)
    # move the charges according to the outfigured vectors
    charges = map(lambda pos, move: validate(np.add(pos, move * min_factor)),charges, forces)
            

def simulate(n):
    global charges
    for i in range(0,n):
        charges = simulateStep()
#simulate(1)

# Grid of x, y points
nx, ny = 64, 64
x = np.linspace(-2, 2, nx)
y = np.linspace(-2, 2, ny)
X, Y = np.meshgrid(x, y)

# Electric field vector, E=(Ex, Ey), as separate components
Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
for charge in charges:
    print(charge)
    ex, ey, _ = E_Field(*charge, (X, Y, 0))
    Ex += ex
    Ey += ey

fig = plt.figure()
ax = fig.add_subplot(111)

def printDistribution():
    for q, pos in charges:
        if(pos[0] == 1):
            ax.add_artist(Circle(pos[1:3], 0.01, color='#0000aa'))
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(-1.1,1.1)
    ax.set_ylim(-1.1,1.1)
    ax.set_aspect('equal')
    plt.show()




def printStreamPlot():
    # Plot the streamlines with an appropriate colormap and arrow style
    color = 2 * np.log(np.hypot(Ex, Ey))
    ax.streamplot(x, y, Ex, Ey, color=color, linewidth=1, cmap=plt.cm.inferno,
                density=3, arrowstyle='->', arrowsize=1.5)
    
    # Add filled circles for the charges themselves
    charge_colors = {True: '#aa0000', False: '#0000aa'}
    for q, pos in charges:
        ax.add_artist(Circle(pos[0:2], 0.01, color=charge_colors[q>0]))
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_aspect('equal')
    plt.show()

printDistribution()
#printStreamPlot()