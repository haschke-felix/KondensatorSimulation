import simulation as sim
import fieldplot as plt
import roundPlateCapacitor as roundCap
import os

if __name__ == '__main__':

    charges = 0.05
    steps =1000
    step = 0.4
    dist = [0.3,0.4,0.6,0.7,0.9,1.2,1.4,1.6,2]
    print(sys.argv)
    

    for d in dist:
        cap = roundCap.setupCapacitor(charges, dist)
        cap = roundCap.simulateThreaded(cap,steps=steps,step=step, dist= dist,savepath=os.getcwd())

