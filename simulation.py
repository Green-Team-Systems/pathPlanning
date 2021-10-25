import time
from utils.position_utils import position_to_list
import setup_path
import airsim

from utils.data_classes import MovementCommand, PosVec3
from path_planning import PathPlanning
from multiprocessing import freeze_support, Queue
import math
from Astar import *
import logging
import traceback

logging.basicConfig(filename="logs/root.log")

if __name__ == "__main__":
    freeze_support()

    # This should match the name of the drone in the settings.json file
    drone_id = "Drone1"

    # When using AirSim, set to true
    simulation = True

    if simulation:
        airsim_client = airsim.MultirotorClient()
        airsim_client.confirmConnection()
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
    logging.info("Test")

    def star_to_move(coords):
        lcomm = []
        for i in range(len(coords)):
            if(i % 5 == 0):
                posTemp = PosVec3(
                    X=coords[i][0],
                    Y=coords[i][1],
                    Z=coords[i][2] - 1
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
    try:
        print(cmds)
        start_time = time.time()
        current_location = dict(X=0.0, Y=0.0, Z=0.0)
        for command in cmds:
            print(command)
            path_planning_queue.put(command)
            arrived = False
            print("Put 1 command")

            while not arrived:
                state = airsim_client.getMultirotorState()
                position = state.kinematics_estimated.position
                current_location["X"] = position.x_val
                current_location["Y"] = position.y_val
                current_location["Z"] = position.z_val
                pos_diff = math.sqrt(pow(current_location["X"] - command.position.X, 2) + pow(current_location["Y"] - command.position.Y, 2))
                if pos_diff < 2.0:
                    arrived = True
                time.sleep(0.5)

    except Exception as error:
        traceback.print_exc()

    # planner.kill()
    airsim_client.reset()
    planner.terminate()
    print("Completed")

