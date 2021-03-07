import simulation as sim
import matplotlib.pyplot as plt
import fieldplot as fplot
import roundPlateCapacitor as roundCap


cap1 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_0.1/roundCap0.05-it1000step0.4dist0.1.npy")
cap2 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_0.2/roundCap0.05-it1000step0.4dist0.2.npy")
cap3 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_0.5/roundCap0.05-it1000step0.4dist0.5.npy")
cap4 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_0.8/roundCap0.05-it1000step0.4dist0.8.npy")
cap5 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_1/roundCap0.05x0.05-it1000step0.4.npy")

print(len(cap1))
fig = plt.figure()
ax = fig.add_subplot(111)
h = 1/18
ax.plot(*fplot.kernelDensityCurve(cap1,h=h), '-', color='green', label="Abstand: 0.1")
ax.plot(*fplot.kernelDensityCurve(cap2,h=h), '-', color='red', label="Abstand: 0.2")
ax.plot(*fplot.kernelDensityCurve(cap3,h=h), '-', color='blue',label="Abstand: 0.5")
ax.plot(*fplot.kernelDensityCurve(cap4,h=h), '--', color='red',label="Abstand: 0.8")
ax.plot(*fplot.kernelDensityCurve(cap5,h=h), '--', color='blue',label="Abstand: 1")

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