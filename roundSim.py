import simulation as sim
import fieldplot as plt
import sys
import roundPlateCapacitor as roundCap

if __name__ == '__main__':

    charges = 0.05
    steps =1000
    print(sys.argv)
    if len(sys.argv) >= 3:
        charges = float(sys.argv[1])
        steps = int(sys.argv[2])
    
    cap = roundCap.setupCapacitor(charges)
    #cap = sim.load("cap50x50-it1000.npy")

    #cap = roundCap.simulateThreaded(cap,steps,step=2)
    for i in range(1,11):
        cap = roundCap.simulateThreaded(cap,100,step=2)
        file = "roundCap{}x{}-it{}.npy".format(charges, charges, i*100)
        sim.save(cap, path=file)
    if(False):
        file = "roundCap{}x{}-it{}.npy".format(charges, charges, steps)
        sim.save(cap, path=file)
    #plt.printStreamPlot(cap,128)
    plt.printDistribution(cap)