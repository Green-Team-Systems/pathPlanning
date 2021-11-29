# =============================================================================
# Created By: Joseph Woo
# Authors: Joseph Woo
# Created On: Nov 29th, 2021
# 
# Description:
# This module is used for testing of the sim, the four parameters to be modified by the user or by the mapping team themselves.
# Should output a 3d scatter plot of the obstacles. 
# =============================================================================

from Star import *
# from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

# Input here:
startCoords  = (60, 70, 60) #<- start
endCoords = (5, 5, 55) #<- end
filename = '3darr.npy'
# End User inputs:

print('start coords')
coords = astar(np.load('3darr.npy'), startCoords, endCoords)
print('end coords')
print(coords)
listo = np.load('3darr.npy')

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
            if(listo[i][j][k]):
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
# ax.scatter3D(xprime, yprime, zprime) # obstacle data
ax.scatter3D(xdata, ydata, zdata) # path data

#ax.scatter3D(xdprime, ydprime, zdprime) # space data
plt.show()
