# pathPlanning
pathplanning algorithm generation for SWARMS

This module is designed to find the most optimal (short) path to a destination or series of destinations with or without a series of obstacles to avoid. It maps a 3D path for the drone given a series of parameters: 
* Numpy 3D Boolean array sent by mapping.
* Starting and Ending Coordinates
* Dimensions of the 3D Boolean array
For now, the weights of dijkstra are simply the distance from one nodes to the next node, IE: Nodes in the up, side, or into direction have weight of 1, Nodes in the diagonal direction in 2d are sqrt(2), and nodes in the 3d diagonal direction are sqrt(3).
## Dependencies:
Pip install:
* airsim modules
* Dijkstar
## Testing:
Run startesting.py, the three values you should manually change are on lines 7, 8, 9: start, end, dimensional coodinates, and filename. Should be given by mapping team. Should output a 3d scatter plot showing the path of the theoretical drone and the obstacle map.

## Relevant Files:
1darr.npy: 100x100x100 dimensional data given by mapping team to test pathplanning algorithm on. - Mapping Team

Astar.py: Actual implementation of dijkstar algorithm given a numpy array file. If no file is ofund, defaults to automatically generated obstacles and generates path through that. - Marvin Mui & Joseph Woo

path_planning.py: Program in which commands to the airsim are sent through, run the airsim, wait for the startup process to finish, and will automatically send commands. - Tyler Fedrizzi

Import this module to automatically setup path to local airsim module
This module first tries to see if airsim module is installed via pip
If it does then we don't do anything else
Else we look up grand-parent folder to see if it has airsim folder and if it does then we add that in sys.path - Tyler Fedrizzi

startesting.py: Used for testing and debugging of the dijkstar and Astar module. Will automatically generate path through the numpy array and will print out and display optimal path using 3d scatter plot. - Joseph Woo

simulation.py: Use to send actual commands to the airsim simulation. -Tyler Fedrizzi & Marvin Mui


By: Marvin Mui, Joseph Woo