import simulation as sim
import fieldplot as plt
import roundPlateCapacitor as roundCap
import easygui
import sys

path = []
if(len(sys.argv) > 1):
    path = sys.argv[1]    
else:
    path ="/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/roundCap0.02x0.02-it1000.npy"
    #path ="/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/roundCap0.05x0.05-it1000step0.4.npy"
    #path = easygui.fileopenbox()
    

cap = sim.load(path)
print(len(cap))
#cap = sim.setupCapacitor(100)
#cap = roundCap.setupCapacitor(0.001)
#cap = roundCap.setupCapacitorAllChargesOnOutline(0.05)

#plt.printDistributionRingsChargesColored(cap)
#plt.chargeOccurancePlot(cap,30)
plt.kernelDensityPlot(cap,sigma=1/40)
#plt.printStreamPlot(cap,256)
#plt.printDistribution(cap)

#plt.strengthInMiddlePlot(cap)