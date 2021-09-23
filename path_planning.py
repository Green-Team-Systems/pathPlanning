# =============================================================================
# Created By: Tyler Fedrizzi
# Authors: Tyler Fedrizzi
# Created On: September 6th, 2020
# Last Modified: Septebmer 5th, 2021
# 
# Description: Module for implementing movement commands to the Aircraft
# =============================================================================

import setup_path
import airsim
import logging
import time
import copy

from multiprocessing import Process
from datetime import datetime
from multiprocessing.queues import Empty

from utils.data_classes import PosVec3, MovementCommand
from utils.killer_utils import GracefulKiller
from airsim.types import YawMode
# TODO Create status library


class PathPlanning(Process):
    """
    A separate process that handles all path planning considerations,
    to include submitting points to the low-level controller, handling
    tracking of the current position and ensuring that all interactions
    are being handled appropriately.

    ## Inputs:
    - queue [Queue] Transmission queue to communicate with main process.
    - drone_id [string] Unique identifier for the UAV
    - user_options [dict] User-defined options for path planning
    - simulation [bool] Determines whether we are running the model with
                        AirSim or not
    """

    def __init__(self, queue, drone_id, user_options=None, simulation=False):
        Process.__init__(self, daemon=True)
        # This is a section of the global map defined by some radius
        # from the drone
        self.local_map = None
        self.drone_id = str(drone_id)
        self.command_queue = queue
        self.simulation = simulation
        # Determining whether we are in the Air or Not
        self.airborne = False
        self.global_map = None
        # Allows for global
        # Use the pre-built map and then use the FOV of the sensors to
        # user map so that they can use it.
        # Client to communicate with AirSim
        self.airsim_client = None
        # TODO Add status updates
        self.status = None
        self.last_command = None
        # TODO Add an inter-process queue between mapping and self
        FORMAT = '%(asctime)s %(message)s'
        # logging.basicConfig(format=FORMAT,
         #                   level=logging.INFO)
        file_handler = logging.FileHandler(
            "logs/{drone_id}-Path-Planning-{date}.log".format(
                drone_id=self.drone_id,
                date=datetime.utcnow()
        ))
        self.log = logging.getLogger(self.drone_id + __name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(file_handler)

    def build_airsim_client(self):
        """
        Generate the AirSim multirotor client, arming the vehicle
        and enabling API control so that the vehicle is ready to take
        commands from the user.

        ## Inputs:
        - None

        ## Outputs:
        - Assigns the multirotor client to the class airsim_client
        variable.
        """
        self.airsim_client = airsim.MultirotorClient()
        self.airsim_client.confirmConnection()
        self.airsim_client.armDisarm(True, self.drone_id)
        self.airsim_client.enableApiControl(True, self.drone_id)
        self.log.info(
            "AirSim API connected. Vehicle is armed and API control is active")

    def generate_trajectory(self, point, velocity, characteristics=[]):
        """

        """
        # point (x,y,z)
        # velocity
        # characteristics = Sneaky, Loud, Specific height,
        #                   Agressive vs. Conserative
        # Sneaky - buffer distance
        # Global creates a trajectory to that point
        # Local handles obstacles between your current position and this point
        # Local updates rapidly from the global map
        pass

    def local_path_trajectory(self):
        # Update rate (defined by our sensor)
        pass

    def fly_to_new_position(self, position: PosVec3, velocity: float) -> None:
        """
        Fly to a new position, receiving the position either directly
        from the main intelligence module or as a component of a path
        planning algorithm.

        Inputs:
        - position [PosVec3] Position to move to, given as X, Y and Z
                             coordinates relative to the body coord.
                             frame of the aircraft.
        - velocity [float] Forward velocity of the quad copter.
        """
        # z_coord = abs(position.Z)
        self.airsim_client.moveToPositionAsync(
            position.X,
            position.Y,
            position.Z,
            velocity,
            vehicle_name=self.drone_id)

    def takeoff(self) -> None:
        """
        Command the UAV to takeoff by making the proper Async call to
        AirSim.
        The client call returns a future and we wait for that future to
        resolve until we continue execution.

        ## Inputs:
        - None

        ## Outputs:
        - Informs the path planning module that the UAV is now
        airborne.
        """
        droneTakeoff = self.airsim_client.takeoffAsync(
            vehicle_name=self.drone_id)
        droneTakeoff.join()
        self.airborne = True
        self.log.info("{}: Takeoff complete. {} is airborne.".format(
            datetime.utcnow(),
            self.drone_id)
        )

    def start(self):
        """
        Override Process start function and update status
        """
        Process.start(self)
        # TODO Update status of operations
    
    def check_for_new_command(self, command: MovementCommand) -> bool:
        """
        Compare the current command to the previous command. If the
        commands are the same ignore that command because it was a
        duplicate given by intelligence module due to processing
        constraints.

        TODO Implement some type of execution status that can be
             tracked by the Intel module so we don't get eroneous
             movement commands.
            
        ## Inputs:
        - command [MovementCommand] The next NED local position to
                                    move to.
        ## Outputs:
        Boolean of whether this is a new command or not
        """
        if self.last_command == None:
            return True

        if (command.position.X == self.last_command.position.X
            and command.position.Y == self.last_command.position.Y
            and command.position.Z == self.last_command.position.Z):
            return False
        else:
            return True

    def receive_commands(self) -> list:
        """
        We constantly need to be checking the command queue to see if
        there are any path planning calls that need to be executed by
        UAV. We listen on the queue, in blocking mode when we are not
        doing other computation, and once we receive a new location, we
        execute that method.

        ## Inputs
        - None

        ## Outputs
        A list of PosVec3 local positions to command the UAV to. It
        could be a set of positions that equal a trajectory or just the
        next point. We ensure generality by not being specific about how
        many points.
        """
        messages = list()
        # This is not reliable. Ideally, we process this async by firing off
        # a command upon every message receipt. This will be implemented later,
        # maybe, depending on how we feel about this.
        # NOTE This doesn't work on MacOS due to:
        # NOTE https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue.qsize
        try:
            num_messages = self.command_queue.qsize()
        except NotImplementedError:
            self.log.debug("MacOS System does not implement _semlock")
            num_messages = 1
        if num_messages > 0:
            for _ in range(num_messages):
                try:
                    messages.append(self.command_queue.get(
                        block=True, timeout=0.0))
                except Empty:
                    continue

        return messages

    def run(self):
        """
        Override of the Process run command to define behavior of the
        path planning module.

        Basic workflow:
        1. Check for a command to build a path
        2. Check for a raw position to be given
        3. If building a path:
            3a. Query map and receieve immediate obstacles
            3b. Build trajectory and store
            3c. Inform control trajecotry generated
        4. Execute trajectory or push next location

        TODO Refactor workflow to use ROS
        """
        Process.run(self)
        killer = GracefulKiller()

        if self.simulation:
            self.build_airsim_client()

        if not self.airborne and self.simulation:
            self.takeoff()
        self.command_queue.put("Takeoff Completed")
        # TODO What if there is a collision or error?

        # Main Execution
        self.log.info("Beginning main path planning execution")
        while not killer.kill_now:
            # Check the queue for commands. Will block until message received.
            commands = self.receive_commands()
            # TODO Add a common inter-process message to either containerize
            # the underlying set of messages or act as a header message for
            # the stream of messages.
            # TODO Add path planning algorithms for processing
            if self.simulation:
                # We will wait for each command to be completed
                for command in commands:
                    self.log.info("{}: {} received {}".format(
                        datetime.utcnow(),
                        self.drone_id,
                        command)
                    )
                    try:
                        assert isinstance(command, MovementCommand)
                        
                        self.move_to_next_position(command)
                        # TODO Send back message on command completion
                        self.log.info(
                            "{}: {} Movement Command Completed: {}".format(
                                datetime.utcnow(),
                                self.drone_id,
                                command
                                )
                            )
                        self.last_command = copy.deepcopy(command)
                    except AssertionError as error:
                        self.log.error("{}: {}".format(
                            datetime.utcnow(),
                            error)
                        )
            else:
                time.sleep(0.1)
        self.log.info("{}: Shutdown initiated!".format(datetime.utcnow()))
        
        # Clean shutdown by disarming and disabling API control
        if self.simulation:
            self.airsim_client.armDisarm(False, vehicle_name=self.drone_id)
            self.airsim_client.enableApiControl(
                False,
                vehicle_name=self.drone_id
            )

        self.log.info("{}: Shutdown completed".format(datetime.utcnow()))

    def move_to_next_position(self, command: MovementCommand) -> bool:
        """
        Given a MovementCommand, send the appropriate AirSim API call
        to move the vehicle in the next direction.

        ## Inputs:
        - command [MovementCommand] data structure containing the pos,
                                    heading and speed of the next pos
                                    of the UAV.
                                    Members:
                                    - position [PosVec3]
                                    - heading [float]
                                    - speed [float]
        ## Outputs
        Boolean that signifies that the execution of the method was
        successful.
        """
        # TODO Add drivetrain once that is fixed
        move_future = self.airsim_client.moveToPositionAsync(
            command.position.X,
            command.position.Y,
            command.position.Z,
            command.speed,
            yaw_mode=YawMode(False,command.heading),
            vehicle_name=self.drone_id
        )
        time.sleep(0.01)
        # move_future.join()
        return True
