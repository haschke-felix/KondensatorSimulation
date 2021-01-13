import simulation as sim
import fieldplot as plt
import easygui

path = easygui.fileopenbox()

cap = sim.load(path)

#plt.printStreamPlot(cap,512)
plt.printDistribution(cap)