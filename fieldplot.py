import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.spatial import distance_matrix
import collections



# Electric field vector, E=(Ex, Ey), as separate components

def _fieldProbe(charges, gridMatrix):
    E = np.zeros(gridMatrix.shape)
    for charge in charges:
        con =  gridMatrix - charge[:,None,None]
        E  +=  con / ((charge[0] * np.linalg.norm(con,axis=0)**3)[None,:,:])
    return E


def printDistribution(charges):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for charge in charges:
        if(charge[0] == 1):
                ax.add_artist(Circle(charge[1:3], 0.01, color='#0000aa'))
    
    #ax.set_xlabel('$x$')
    #ax.set_ylabel('$y$')
    ax.set_xlim(-1.1,1.1)
    ax.set_ylim(-1.1,1.1)
    ax.set_aspect('equal')
    plt.axis('off')

    fig.tight_layout()
    plt.show()


def printDistributionRingsChargesColored(charges, sections = 10):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # create concentric rings:
    for i in range (1,sections+1):
        print(i)
        ax.add_artist(Circle((0,0), (sections + 1- i) / sections , color= '#ded9d9' if i % 2 == 1 else '#ffffff'))
    

    for charge in charges:
        if(charge[0] == 1):
                color = '#eb2121'
                if np.floor((sections) * np.linalg.norm(charge[1:3])) % 2 == 0:
                    color = '#2b21eb'
                ax.add_artist(Circle(charge[1:3], 0.01, color=color))
    
    #ax.set_xlabel('$x$')
    #ax.set_ylabel('$y$')
    ax.set_xlim(-1.1,1.1)
    ax.set_ylim(-1.1,1.1)
    ax.set_aspect('equal')
    plt.axis('off')

    fig.tight_layout()
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
                density=1.6, arrowstyle='->', arrowsize=1.5)
    
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_aspect('equal')

    # Turn off tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Add filled circles for the charges themselves
    charge_colors = {True: '#aa0000', False: '#0000aa'}
    for charge in charges:
        ax.add_artist(Circle(charge[0:2], 0.02, color=charge_colors[charge[0]>0]))
    
    plt.show()


def strengthInMiddlePlot(charges, res=1000, range=5):
    x = np.linspace(-range,range,res)
    points = np.array((x,np.zeros(res),np.zeros(res)))
    

    E = np.zeros(points.shape)
    for charge in charges:
        con =  charge[:,None] - points
        E  +=  con / ((charge[0]  * np.linalg.norm(con,axis=0)**3)[None,:])
    print(E[0])

    # turn into percentage value
    E /= E[0].max()
    E *= 100

    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.plot(x,E[0], '-', color='black')
    ax.set_xlabel("$x_1 \\, (m)$")
    ax.set_ylabel("$E_0 \\, (\\%)$")
    
    x1 = np.linspace(-range, range, 2)
    y1 = np.zeros(x1.shape)
    
    ax.plot(x1,y1) 

    plt.show()

def kernel(r,x,sigma):
    return np.exp(-((r-x)/sigma)**2) / r


# only properly working for round cap
def kernelDensityPlot(charges,res=1000,sigma=1/40):
    # figure all radiuses
    positivePlate = charges[charges[:,0] > 0]
    r = np.hypot(positivePlate[:,1],positivePlate[:,2])
    #r = np.concatenate((r, -1*r))

    x = np.linspace(0,1,res)
    y = np.zeros(res)
        
    i = 0
    integral = 0

    for xval in x:

        y[i] = kernel(r, np.full((r.shape),xval),sigma).sum()
        integral += y[i]
        i += 1
    y /= (integral / res)
    
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.plot(x,y, '-', color='black')
    #ax.set_xlabel("$x_1 \\, (m)$")
    #ax.set_ylabel("$E_0 \\, (\\%)$")
    
    #x1 = np.linspace(-range, range, 2)
    #y1 = np.zeros(x1.shape)
    
    #ax.plot(x1,y1) 

    plt.show()


# only properly working for round cap
def chargeOccurancePlot(charges,res=10):
    # figure all radiuses
    positivePlate = charges[charges[:,0] > 0]
    r = np.hypot(positivePlate[:,1],positivePlate[:,2])

    col = collections.Counter((res*r).round(0))
    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = np.array(list(col.keys())) / res
    y = np.array(list(col.values())) / x
    y /= (y.sum() / res)

    print(y.sum())

    ax.bar(x, y, width=0.8 / res)
    
    #plt.axis('off')
    plt.margins()
    plt.show()