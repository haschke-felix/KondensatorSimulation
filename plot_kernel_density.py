import simulation as sim
import matplotlib.pyplot as plt
import fieldplot as fplot
import roundPlateCapacitor as roundCap


start = roundCap.setupCapacitor(0.02)
cap = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.02/Breite_1.0/cap.npy")


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(*fplot.kernelDensityCurve(cap,h=1/50), '-', color='black', label="Bandbreite $h = \frac{1}{40}$")
ax.plot(*fplot.kernelDensityCurve(cap,h=1/100), '-', color='red', label="Bandbreite $h = \frac{1}{40}$")

#ax.set_xlabel("$r$")
#ax.set_ylabel("$\~\p(r)$")
#ax.set_xlim(0,1)

plt.legend()
plt.show()