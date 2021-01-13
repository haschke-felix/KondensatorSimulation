import simulation as sim
import fieldplot as plt

cap = sim.setupCapacitor(20)
cap = sim.simulate(cap,10)

plt.printStreamPlot(cap,n=512)
