import simulation as sim
import fieldplot as plt
import easygui
import sys

path = []
if(len(sys.argv) > 1):
    path = sys.argv[1]    
else:
    path = easygui.fileopenbox()
    

cap = sim.load(path)

plt.printStreamPlot(cap,2048)
#plt.printDistribution(cap)