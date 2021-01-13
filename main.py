import simulation as sim
import fieldplot as plt

cap = sim.load("cap.npy")
#cap = sim.setupCapacitor(20)
#cap = sim.simulate(cap,10)
print(cap)

#sim.save(cap,"cap.npy")

#plt.printDistribution(cap)
plt.printStreamPlot(cap,n=64)
