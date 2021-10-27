from Astar import *
# from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

startCoords  = [0, 0, 0]
endCoords = [100, 100, 0]
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
for i in range(30, 45):
    for j in range(30, 45):
        for k in range (0, 1):
            xprime.append(i)
            yprime.append(j)
            zprime.append(k)
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(xdata, ydata, zdata)
ax.scatter3D(xprime, yprime, zprime)
plt.show()
