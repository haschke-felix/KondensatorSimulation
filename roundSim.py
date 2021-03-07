import simulation as sim
import fieldplot as plt
import sys
import roundPlateCapacitor as roundCap

def fileName(charges, it, step,dist):
    return  "roundCap{}-it{}step{}dist{}.npy".format(charges, it,step, dist)

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
    #cap = sim.load("cap50x50-it1000.npy")

    #cap = roundCap.simulateThreaded(cap,steps,step=2)
    for i in range(1,int (steps / 100) + 1):
        cap = roundCap.simulateThreaded(cap,100,step=step)
        file = fileName(charges, i*100,step,dist)
        sim.save(cap, path=file)
    if(False):
        file = fileName(charges, steps,step,dist)
        sim.save(cap, path=file)
    #plt.printStreamPlot(cap,128)
    plt.printDistribution(cap)