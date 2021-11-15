# pathPlanning
pathplanning algorithm generation for SWARMS

This module is designed to find the most optimal path to a destination or series of destinations with or without a series of obstacles to avoid.

## Relevant Files:
1darr.npy: 100x100x100 dimensional data given by mapping team to test pathplanning algorithm on.

Astar.py: Actual implementation of dijkstar algorithm given a numpy array file. If no file is ofund, defaults to automatically generated obstacles and generates path through that.

path_planning.py: Program in which commands to the airsim are sent through, run the airsim, wait for the startup process to finish, and will automatically send commands.

setup_path.py: see's if airsim is up and exists.

startesting.py: Used for testing and debugging of the dijkstar and Astar module. Will automatically generate path through the numpy array and will print out and display optimal path using 3d scatter plot. 

## Commands

By: Marvin Mui, Joseph Woo