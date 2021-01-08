import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def norm(x,y,z):
    return np.sqrt(x*x+y*y+z*z)

def E(q, r0, p):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    den = norm(p[0]-r0[0], p[1]-r0[1],p[2]-r0[2])**3
    return q * (p[0] - r0[0]) / den, q * (p[1] - r0[1]) / den, q * (p[2] - r0[2]) / den




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

def simulateStep():
    moved_charges = []
    for qp, posp in charges:
        Ey, Ez = 0, 0 # Ex not relevant for movement on the plate
        for q, pos in charges:
            if(posp != pos):
                _, ey, ez = E(q,pos, posp) # ex is not necessary again
                Ey += ey
                Ez += ez
        #print("Ey: ",Ey)
        #print("Ez: ",Ez)
        py = factor*Ey*qp + posp[1]
        if(py < -1): py = -1
        if(py > 1): py=1
        pz = factor*Ez*qp + posp[2]
        if(pz < -1): pz = -1
        if(pz > 1): pz=1
        moved_charge = (qp,(posp[0],py,pz))
        moved_charges.append(moved_charge)
    return moved_charges

def simulate(n):
    global charges
    for i in range(0,n):
        charges = simulateStep()
simulate(100)

# Grid of x, y points
nx, ny = 64, 64
x = np.linspace(-2, 2, nx)
y = np.linspace(-2, 2, ny)
X, Y = np.meshgrid(x, y)

# Electric field vector, E=(Ex, Ey), as separate components
Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
for charge in charges:
    ex, ey, _ = E(*charge, (X, Y, 0))
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

#printDistribution()
printStreamPlot()