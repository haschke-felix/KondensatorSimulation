import simulation as sim
import fieldplot as plt
import sys
import roundPlateCapacitor as roundCap
import os

if __name__ == '__main__':

    charges = 0.1
    steps =1000
    step = 0.4
    dist = 0.5
    print(sys.argv)
    
    try:
        charges = float(sys.argv[1]) 
    except (IndexError):
        pass
    try:
        steps = int(sys.argv[2])
    except (IndexError):
        pass
    try:
        step = float(sys.argv[3]) 
    except(IndexError): 
        pass
    try:
        dist = float(sys.argv[4]) 
    except(IndexError): 
        pass

    cap = roundCap.setupCapacitor(charges, dist)

    cap = roundCap.simulateThreaded(cap,steps=steps,step=step, dist= dist,savepath=os.getcwd())

    #plt.printStreamPlot(cap,128)
    plt.printDistribution(cap)

