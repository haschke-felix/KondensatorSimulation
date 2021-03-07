import simulation as sim
import matplotlib.pyplot as plt
import fieldplot as fplot
import roundPlateCapacitor as roundCap


start = roundCap.setupCapacitor(0.015)
cap1 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/roundCap0.1x0.1-it1000.npy")
cap2 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/roundCap0.05x0.05-it1000step0.4.npy")
cap3 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/Steps/0,02/roundCap0.02x0.02-it1000.npy")
cap4 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/roundCap0.015x0.015-it700step0.4.npy")

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(*fplot.kernelDensityCurve(cap1,h=1/12), '-', color='green', label="283 Ladungen")
ax.plot(*fplot.kernelDensityCurve(cap2,h=1/18), '-', color='red', label="1194 Ladungen")
ax.plot(*fplot.kernelDensityCurve(cap3,h=1/40), '-', color='blue',label="7697 Ladungen")
#ax.plot(*fplot.kernelDensityCurve(cap4,h=1/12), '-', color='black',label="13892 Ladungen")

#1/12
#1/18
#1/40
#1/70

ax.set_xlabel("$r$")
ax.set_ylabel("$\~\sigma\, (r)$")
ax.set_xlim(0,1)

plt.legend()
plt.show()