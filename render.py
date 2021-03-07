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
    #path = easygui.fileopenbox(default="/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund")
    
#cap = sim.load(path)
cap1 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/roundCap0.1x0.1-it1000.npy")
cap2 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/Steps/0,1_neu/roundCap0.1x0.1-it1000step0.4.npy")
#print(len(cap))
#cap = sim.setupCapacitor(100)
#cap = roundCap.setupCapacitor(0.001)
#cap = roundCap.setupCapacitorAllChargesOnOutline(0.05)

#plt.printDistributionRingsChargesColored(cap)
#plt.chargeOccurancePlot(cap,30)
#plt.kernelDensityPlot(cap,h=1/40)
plt.compareDensity(cap1,cap2,h1=1/12,h2=1/12,label1="Alt",label2="Neu")
#plt.printStreamPlot(cap,256)
#plt.printDistribution(cap)

#plt.strengthInMiddlePlot(cap)