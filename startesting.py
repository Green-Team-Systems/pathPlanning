from Astar import *
# from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

startCoords  = (3, 3, 6)
endCoords = (11, 11, 8)
pathPlan = Astar()
coords = pathPlan.DApath(startCoords, endCoords, '1darrData.npy', [0, 20, 0, 20, 0, 20])
print(coords)
listo = np.load('1darrData.npy')

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
xdprime = []
ydprime = []
zdprime = []
print(len(listo))
for i in range(0, 19):
    for j in range(0, 19):
        for k in range (0, 19):
            if(listo[i*400+j*20+k]):
                bye = 1
                #xprime.append(i)
                #yprime.append(j)
                #zprime.append(k)
            else:
                xdprime.append(i)
                ydprime.append(j)
                zdprime.append(k)
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(xdata, ydata, zdata)
ax.scatter3D(xprime, yprime, zprime)
ax.scatter3D(xdprime, ydprime, zdprime)
plt.show()
