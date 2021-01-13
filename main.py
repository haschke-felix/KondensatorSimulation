import simulation as sim
import fieldplot as plt

charges = 10
steps = 1000

cap = sim.setupCapacitor(charges)
cap = sim.simulate(cap,steps)

file = "cap{}x{}-it{}.npy".format(charges, charges, steps)

sim.save(cap, path=file)

plt.printStreamPlot(cap,512)
