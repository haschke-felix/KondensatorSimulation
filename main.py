import simulation as sim
import fieldplot as plt
import threadedSim

if __name__ == '__main__':

    charges = 10
    steps = 50
    cap = sim.setupCapacitor(charges)
    #print("created")
    #
    #th = threadedSim.ThreadedSim(cap)
    #cap = th.run()
    #print("threaded ready")
    
    
    cap = sim.simulate(cap,steps)
    
    file = "cap{}x{}-it{}.npy".format(charges, charges, steps)
    
    sim.save(cap, path=file)
    
    plt.printStreamPlot(cap,512)
