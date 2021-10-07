from queue import Queue
from utils.data_classes import MovementCommand, PosVec3
from path_planning import PathPlanning

# This should match the name of the drone in the settings.json file
drone_id = "Drone1"

# When using AirSim, set to true
simulation = False

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

# End position user requests
cmds.append(MovementCommand(
    position=PosVec3(
        X=100,
        Y=100,
        Z=-20
    ),
    heading=90,
    speed=6.0
))

for command in cmds:
    path_planning_queue.put(command)
