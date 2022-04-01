# =============================================================================
# Created By: Joseph Woo
# Authors: Joseph Woo
# Created On: October 27th, 2021
# Last Modified: November 18th, 2021
# 
# Description:
# This module is used for testing of the sim, the four parameters to be modified by the user or by the mapping team themselves.
# Should output a 3d scatter plot of the obstacles. 
# =============================================================================

from Astar import *
# from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

# Input here:
startCoords  = (60, 70, 60) #<- start
endCoords = (5, 5, 55) #<- end
dimensions = [0, 100, 0, 100, 0, 100] #<- dimensions of the map
filename = '1darr.npy'
# End User inputs:


pathPlan = Astar()
coords = pathPlan.DApath(startCoords, endCoords, filename, dimensions)
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
#ax.scatter3D(xprime, yprime, zprime) # obstacle data
ax.scatter3D(xdata, ydata, zdata) # path data

#ax.scatter3D(xdprime, ydprime, zdprime) # space data
plt.show()
