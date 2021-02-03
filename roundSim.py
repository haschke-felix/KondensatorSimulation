import simulation as sim
import fieldplot as plt
import sys
import roundPlateCapacitor as roundCap

if __name__ == '__main__':

    charges = 0.1
    steps =1000
    step = 0.4
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
    
    cap = roundCap.setupCapacitor(charges)
    #cap = sim.load("cap50x50-it1000.npy")

    #cap = roundCap.simulateThreaded(cap,steps,step=2)
    for i in range(1,int (steps / 100) + 1):
        cap = roundCap.simulateThreaded(cap,100,step=step)
        file = "roundCap{}x{}-it{}step{}.npy".format(charges, charges, i*100,step)
        sim.save(cap, path=file)
    if(False):
        file = "roundCap{}x{}-it{}step{}.npy".format(charges, charges, steps,step)
        sim.save(cap, path=file)
    #plt.printStreamPlot(cap,128)
    plt.printDistribution(cap)