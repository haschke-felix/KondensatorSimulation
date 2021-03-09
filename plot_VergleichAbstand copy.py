import simulation as sim
import matplotlib.pyplot as plt
import fieldplot as fplot
import roundPlateCapacitor as roundCap
import numpy as np

widths = np.array([0.05, 0.3,0.5,1.0])
colors = [('-', 'green'),('-', 'red'),('-', 'blue'),('-', 'orange'), ('-', 'black')]

caps = []
h = 1/80
for w in widths:
    path = "/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.02/Breite_{}/cap.npy".format(w)
    print(path) 
    cap = sim.load(path)
    caps.append(fplot.kernelDensityCurve(cap,h=h))

fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(0, min(len(colors),len(caps))):
    ax.plot(*caps[i], colors[i][0], color=colors[i][1], label="Abstand: {}".format(widths[i]*2))   

# limit curve
#inf = sim.load("/home/felix/Documents/Schule/Physik/Facharbeit/Research/Python/Simuliert/rund/0.05/Breite_10000.0/cap.npy")
#ax.plot(*fplot.kernelDensityCurve(inf,h=h), '--', color='black', label="Abstand: ꝏ")

# intersection
def intersections(x, f, g):
    idx = np.argwhere(np.diff(np.sign(f - g))).flatten()
    return x[idx], f[idx]

def allIntersections():
    x = caps[0][0]
    sects = []
    sectsy = []
    for i in range(0,len(caps)-1):
        for j in range (i+1, len(caps)):
            print(i,j)
            f = caps[i][1]
            g = caps[j][1]
            sect = intersections(x,f,g)
            if(sect[0].size):
                sects.append(sect[0][0])
                sectsy.append(sect[1][0])
            plt.plot(*sect, 'ro')
    print(sects)
    print("min:", min(sects), "max:", max(sects))
    print(sectsy)
    print("average: ", sum(sectsy) / len(sectsy))

#allIntersections()

ax.set_xlabel("$r$")
ax.set_ylabel("$\~\sigma\, (r)$")
ax.set_xlim(0,1)

plt.legend()
plt.show()

