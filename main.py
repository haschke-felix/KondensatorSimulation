import simulation as sim
import fieldplot as plt
import sys
import roundPlateCapacitor as roundCap

if __name__ == '__main__':

    charges = 10
    steps = 100
    print(sys.argv)
    if len(sys.argv) >= 3:
        charges = int(sys.argv[1])
        steps = int(sys.argv[2])
    #cap = sim.setupCapacitor(charges)
    cap = sim.load("cap50x50-it1000.npy")

    cap = sim.simulateThreaded(cap,steps,step=2)
    
    file = "cap{}x{}-it{}.npy".format(charges, charges, 1000+steps)
    
    sim.save(cap, path=file)
    
    #plt.printStreamPlot(cap,512)
    plt.printDistribution(cap)