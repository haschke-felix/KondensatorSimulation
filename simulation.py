import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from enum import Enum
from scipy.spatial import distance_matrix

def E_Field(q, r0, p):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    connection = np.subtract(p,r0)
    den = np.linalg.norm(connection)**3
    return q * connection / den

def E_FieldMatrix(r0, p):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    connection = np.subtract(p,r0[:,np.newaxis,np.newaxis])
    den = np.linalg.norm(connection,axis=0)**3
    return r0[0] * connection / den



# setup capacitor
clen = 10

cy = np.linspace(-1, 1,num=clen,endpoint=True)
cz = np.linspace(-1, 1,num=clen,endpoint=True)
Cy, Cz = np.meshgrid(cy, cz)
plateplus = np.array((np.full((clen,clen),1),Cy,Cz))
plateminus = np.array((np.full((clen,clen),-1),Cy,Cz))
charges = np.concatenate((plateplus,plateminus),axis=1).reshape(3,-1).swapaxes(0,1)
#print(charges)
charges  = plateplus.reshape(3,-1).swapaxes(0,1)
print(charges)

class SurfaceState(Enum):
    OnSurface = 1
    OnOutline = 2
    Outside = 3

def surfaceOption(pos):
    if(abs(pos[0]) > 1 or abs(pos[1]) > 1):
        return SurfaceState.Outside
    if(np.isclose(abs(pos[0]),1) or np.isclose(abs(pos[1]),1)):
        return SurfaceState.OnOutline
    return SurfaceState.OnSurface

def validate (pos):
    if (not np.isclose(abs(pos[1]),1)) and abs(pos[1]) > 1:
        pos[1] = -1 if pos[1] < 0 else 1
    if (not np.isclose(abs(pos[2]),1)) and abs(pos[2]) > 1:
        pos[2] = -1 if pos[2] < 0 else 1
    return pos

fraction = 0.4

def simulateStep():
    min_factor = 1
    E = np.zeros((len(charges),3))
    for i in range(0,len(charges)):
        # evaluate single field
        charge = charges[i]
        connections = np.subtract(charge,charges)
        print("connections", connections)
        distances = np.linalg.norm(connections,axis=1)
        print("distances: ", distances)
        #print("charges:",(charges.swapaxes(0,1)[0])[:,np.newaxis] * np.ones((32,3)))
        #print("rest:", connections / (charges.swapaxes()[0] * (distances**3))[:,np.newaxis])
        E[i] = charge[0] * np.ma.masked_invalid(connections / (charges.swapaxes(0,1)[0] * (distances**3))[:,np.newaxis]).sum()
        E[i][0] = 0
        tmpE = E[i]

        min_dist = np.amin(np.ma.masked_equal(distances, 0))
                
        min_factor = min(min_factor, fraction * min_dist / np.linalg.norm(tmpE))
        tmp_pos = np.add(charge, min_factor * tmpE)
        # if currently considered point is outside range, additional steps have to be performed
        if surfaceOption(tmp_pos) == SurfaceState.Outside:
            opt = surfaceOption(charge)
            if opt == SurfaceState.OnOutline:
                # only consider the tangential field
                if np.isclose(abs(charge[1]),1):
                    E[1] = 0
                if np.isclose(abs(charge[2]),1):
                    E[2] = 0
            if opt == SurfaceState.OnSurface:
                # only move till on Outline --> figure out intersection
                # handle x / [1] component
                border = (1 if tmpE[1] > 0 else -1) - charge[1]
                len_y = np.linalg.norm((border * tmpE[1] / tmpE[2],border))
                border = (1 if tmpE[2] > 0 else -1) - charge[2]
                len_x = np.linalg.norm((border * tmpE[2] / tmpE[1], border))
                min_factor = min(min_factor, min(len_x, len_y) / np.linalg.norm(tmpE))
        
    print(min_factor)
    # move the charges according to the outfigured vectors

    return np.apply_along_axis(validate ,1,charges + E * min_factor)

def simulate(n):
    global charges
    for i in range(0,n):
        print("...", i, "...")
        charges = simulateStep()
simulate(1)

# Grid of x, y points
nx, ny = 64, 64
x = np.linspace(-2, 2, nx)
y = np.linspace(-2, 2, ny)
X, Y = np.meshgrid(x, y)
Z = np.zeros((nx,ny))
gridMatrix = np.array((X,Y,Z))

# Electric field vector, E=(Ex, Ey), as separate components
E = np.array((np.zeros((ny, nx)), np.zeros((ny, nx)), np.zeros((ny, nx))))
for charge in charges:
    E += E_FieldMatrix(charge, gridMatrix)

fig = plt.figure()
ax = fig.add_subplot(111)

def printDistribution():
    for charge in charges:
        if(charge[0] == 1):
                ax.add_artist(Circle(charge[1:3], 0.01, color='#0000aa'))
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(-1.1,1.1)
    ax.set_ylim(-1.1,1.1)
    ax.set_aspect('equal')
    plt.show()




def printStreamPlot():
    # Plot the streamlines with an appropriate colormap and arrow style
    color = 2 * np.log(np.hypot(E[0],E[1]))
    ax.streamplot(x, y, E[0], E[1], color=color, linewidth=1, cmap=plt.cm.inferno,
                density=3, arrowstyle='->', arrowsize=1.5)
    
    # Add filled circles for the charges themselves
    charge_colors = {True: '#aa0000', False: '#0000aa'}
    for charge in charges:
        ax.add_artist(Circle(charge[0:2], 0.01, color=charge_colors[charge[0]>0]))
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_aspect('equal')
    plt.show()

printDistribution()
#printStreamPlot()