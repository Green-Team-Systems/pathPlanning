from utils.data_classes import MovementCommand, PosVec3
from path_planning import PathPlanning
from multiprocessing import freeze_support, Queue
import math
from Astar import *

if __name__ == "__main__":
    # freeze_support()

    # This should match the name of the drone in the settings.json file
    drone_id = "Drone1"

    # When using AirSim, set to true
    simulation = True

    # Vehicle has taken off
    takeoff_completed = False

    path_planning_queue = Queue()

    planner = PathPlanning(path_planning_queue,
                        drone_id,
                        simulation=simulation)

    # The process is running separately of this process
    planner.start()

    while not takeoff_completed:
        try:
            message = path_planning_queue.get(block=True, timeout=0.0)
            if message == "Takeoff Completed":
                takeoff_completed = True
            # TODO Handle takeoff failures
        except Exception:
            pass

    cmds = list()


    def star_to_move(coords):
        lcomm = list()
        for i in range(len(coords)):
            if(i % 5 == 0):
                posTemp = PosVec3(
                    X=coords[i][0],
                    Y=coords[i][1],
                    Z=coords[i][2]
                )
                if coords[i][0] != 0:
                    calcheading = math.atan(coords[i][1]/coords[i][0])
                else:
                    calcheading = 90

                speed = 5.0
                mvmCmd = MovementCommand(position = posTemp, heading = 0, speed=5.0)
                lcomm.append(mvmCmd)
                print("Appended new movement command to lcomm")
        return lcomm

    startCoords  = [0, 0, 0]
    endCoords = [100, 100, 22]
    pathPlan = Astar()
    coords = pathPlan.DApath(startCoords, endCoords)

    cmds = star_to_move([(0, 0, 0), (0, 1, 0), (0, 2, 0), (0, 98, 0), (0, 99, 0), (0, 100, 0)])
    # End position user requests
    # cmds.append(MovementCommand(
    #    position=PosVec3(
    #        X=100,
    #        Y=100,
    #        Z=-20
    #    ),
    #    heading=90,
    #    speed=6.0
    #))

    for command in cmds:
        path_planning_queue.put(command)
        print("Put 1 command")


