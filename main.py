import simulation as sim
import fieldplot as plt
import sys

if __name__ == '__main__':

    charges = 10
    steps = 10
    print(sys.argv)
    if len(sys.argv) >= 3:
        charges = int(sys.argv[1])
        steps = int(sys.argv[2])
    cap = sim.setupCapacitor(charges)
 
    cap = sim.simulateThreaded(cap,steps)
    
    file = "cap{}x{}-it{}.npy".format(charges, charges, steps)
    
    sim.save(cap, path=file)
    
    #plt.printStreamPlot(cap,512)
    plt.printDistribution(cap)