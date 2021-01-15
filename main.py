import simulation as sim
import fieldplot as plt
import sys

if __name__ == '__main__':

    charges = 10
    steps = 10
    if len(sys.argv) >= 2:
        charges = sys.argv[0]
        steps = sys.argv[1]
    cap = sim.setupCapacitor(charges)
 
    cap = sim.simulateThreaded(cap,steps)
    
    file = "cap{}x{}-it{}.npy".format(charges, charges, steps)
    
    sim.save(cap, path=file)
    
    #plt.printStreamPlot(cap,512)
    plt.printDistribution(cap)