import simulation as sim
import fieldplot as plt

cap = sim.setupCapacitor(10)
cap = sim.simulate(cap,10)

plt.printStreamPlot(cap)
