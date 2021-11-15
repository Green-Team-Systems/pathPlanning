from Astar import *
# from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

startCoords  = (60, 70, 70)
endCoords = (60, 5, 60)
pathPlan = Astar()
coords = pathPlan.DApath(startCoords, endCoords, '1darr.npy', [0, 100, 0, 100, 0, 100])
print(coords)
listo = np.load('1darr.npy')

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
for i in range(0, 99):
    for j in range(0, 99):
        for k in range (0, 99):
            if(listo[i*10000+j*100+k]):
                xprime.append(i)
                yprime.append(j)
                zprime.append(k)
            #else:
                #xdprime.append(i)
                #ydprime.append(j)
                #zdprime.append(k)

    print(i)
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(xdata, ydata, zdata)
#ax.scatter3D(xprime, yprime, zprime)
#ax.scatter3D(xdprime, ydprime, zdprime)
plt.show()
