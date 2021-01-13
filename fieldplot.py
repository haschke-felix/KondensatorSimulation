import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.spatial import distance_matrix


def E_FieldMatrix(r0, p):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    connection = np.subtract(p,r0[:,np.newaxis,np.newaxis])
    den = np.linalg.norm(connection,axis=0)**3
    return r0[0] * connection / den

# Electric field vector, E=(Ex, Ey), as separate components

def _fieldProbe(charges, gridMatrix):
    try:
        con = charges.swapaxes(0,1)[:,None,None,:] - gridMatrix[:,:,:,None]
        den = con[0,:,:,:] *  (np.linalg.norm(con,axis=0)**3)
        return np.ma.masked_invalid(con / con[0,:,:,:] *  (np.linalg.norm(con,axis=0)**3)).sum(axis=3)
    except MemoryError:
        E = np.zeros(gridMatrix.shape)
        for charge in charges:
            con = gridMatrix - charge[:,None,None]
            E  +=  con / (charge[0] * np.linalg.norm(con,axis=0))
        return E
    

    
    #connections = np.subtract(charge,charges)
    #distances = np.linalg.norm(connections,axis=1)
    #E[i] = charge[0] * np.ma.masked_invalid(connections / (charges.swapaxes(0,1)[0] * (distances**3))[:,np.newaxis]).sum(axis=0)
    #E[i][0] = 0 # necessary in order keep charges on plate 
    #tmpE = E[i]


def printDistribution(charges):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for charge in charges:
        if(charge[0] == 1):
                ax.add_artist(Circle(charge[1:3], 0.01, color='#0000aa'))
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(-1.1,1.1)
    ax.set_ylim(-1.1,1.1)
    ax.set_aspect('equal')
    plt.show()


def printStreamPlot(charges,n=512):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # generate grid
    print("generating grid")
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros((n,n))
    gridMatrix = np.array((X,Y,Z))

    E = _fieldProbe(charges, gridMatrix)
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