import simulation as sim
import matplotlib.pyplot as plt
import fieldplot as fplot
import roundPlateCapacitor as roundCap


start = roundCap.setupCapacitor(0.02)
cap1 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.02/Breite_1.0/steps/roundCap0.02x0.02-it100.npy")
cap2 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.02/Breite_1.0/steps/roundCap0.02x0.02-it400.npy")
cap3 = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.02/Breite_1.0/cap.npy")


fig = plt.figure()
ax = fig.add_subplot(111)
h= 1/65
ax.plot(*fplot.kernelDensityCurve(start,h=h), '--', color = 'black', label="Start-Konfiguration")
ax.plot(*fplot.kernelDensityCurve(cap1,h=h), '-', color='green', label="100 Schritte")
ax.plot(*fplot.kernelDensityCurve(cap2,h=h), '-', color='red', label="400 Schritte")
ax.plot(*fplot.kernelDensityCurve(cap3,h=h), '-', color='blue',label="1000 Schritte")

ax.set_xlabel("$r$")
ax.set_ylabel("$\~\sigma(r)$")
ax.set_xlim(0,1)

plt.legend()
plt.show()