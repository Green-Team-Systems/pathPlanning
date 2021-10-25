from Astar import *
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

startCoords  = [0, 0, 0]
endCoords = [20, 20, 20]
pathPlan = Astar()
coords = pathPlan.DApath(startCoords, endCoords)
print(coords)

xdata = []
ydata = []
zdata = []
for x in coords:
    xdata.append(x[0])
    ydata.append(x[1])
    zdata.append(x[2])
xprime = []
yprime = []
zprime = []
for i in range(0, 5):
    for j in range(0, 5):
        for k in range (3, 5):
            xprime.append(i)
            yprime.append(j)
            zprime.append(k)
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(xdata, ydata, zdata)
ax.scatter3D(xprime, yprime, zprime)
plt.show()
