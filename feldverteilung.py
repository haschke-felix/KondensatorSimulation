import numpy as np
import simulation as sim
import fieldplot as fplot
import roundPlateCapacitor as roundCap
import easygui
import sys

resolution = 200
if(len(sys.argv) > 1):
    resolution = int(sys.argv[1])    


def _fieldProbe(charges, gridMatrix):
    con = np.subtract(gridMatrix[:,:,:,:,None], charges[:,None,None,None,:],axis=0)
    E = con / (charges[:,])
    for charge in charges:
        con =  gridMatrix - charge[:,None,None,None]
        E  +=  con / ((charge[0] * np.linalg.norm(con,axis=0)**3)[None,:,:,:])
    return E

def distributionAnalysis(charges,n=512, r=2, dist=1):
    # generate grid
    print("generating grid")
    p1 = np.linspace(-r, r, n)
    p2 = np.linspace(-r, r, n)
    p3 = np.linspace(-r, r, n)

    print("generating field matrix")
    gridMatrix = np.array(np.meshgrid(p1, p2, p3, indexing = 'ij'))
    print("calculating field")
    E = np.linalg.norm(_fieldProbe(charges, gridMatrix),axis=0)
    
    print("evaluating sum")
    cap_sum = 0
    sum = E.sum()

    for x_1 in range(0, n):
        print(x_1)
        if p1[x_1] < -dist or p1[x_1] > dist:
            continue
        for x_2 in range(0, n):
            if p2[x_2] > 1:
                continue
            for x_3 in range(0, n):
                if np.hypot(p3[x_2], p3[x_3]) < 1:
                    cap_sum += E[x_1][x_2][x_3]
    print("total: ", sum)
    print("in capacitor", cap_sum)
    print("quotient", cap_sum / sum)




path = easygui.fileopenbox(default="/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund")
#path = "/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.02/Breite_1.0/cap.npy"
cap = sim.load(path)

distributionAnalysis(cap,n=resolution,r=10, dist=0.4)