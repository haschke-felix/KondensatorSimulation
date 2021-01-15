import simulation as sim
import fieldplot as plt

if __name__ == '__main__':

    charges = 50
    steps = 50
    cap = sim.setupCapacitor(charges)
    #print("created")
    #
    #th = threadedSim.ThreadedSim(cap)
    #cap = th.run()
    #print("threaded ready")
    
    
    cap = sim.simulateThreaded(cap,steps)
    
    file = "cap{}x{}-it{}.npy".format(charges, charges, steps)
    
    sim.save(cap, path=file)
    
    #plt.printStreamPlot(cap,512)
    plt.printDistribution(cap)