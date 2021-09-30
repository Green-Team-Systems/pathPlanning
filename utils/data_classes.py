# ===============================================================
# Copyright 2021. Codex Laboratories LLC
# Created By: Tyler Fedrizzi
# Authors: Tyler Fedrizzi
# Created On: August 18th, 2021
# Updated On: August 18th, 2021
# 
# Description: Data classes for ease of use
# ===============================================================

from dataclasses import dataclass
from math import sqrt


@dataclass
class PosVec3:
    """
    Position vector containing the X, Y and Z coordinates as defined
    in an Earth-Center, Earth Facing global coordinate system.

    Units are Meters.

    Members are:
    - X: X coordinate of the ECEF coordinate system
    - Y: Y coordinate of the ECEF coordinate system
    - Z: Z coordinate of the ECEF coordinate system
    """
    X: float = 0.0
    Y: float = 0.0
    Z: float = 0.0
    frame: str = "local"


@dataclass
class GPSPosVec3:
    """
    Position vector containing the Latitude, Longitude and Altitude
    coordinates as defined in an elliptical spheriod Earth model.

    Units are Meters.

    Members are:
    - Lat: Latitude of the current vehicle in degrees
    - Lon: Longitude of the current vehicle in degrees
    - Alt: Altitude of the current vehicle in meter
    """
    Lat: float = 0.0
    Lon: float = 0.0
    Alt: float = 0.0


@dataclass
class VelVec3:
    """
    Velocity vector containing the X, Y and Z velocities as measured
    relative to the body frame of the vehicle.

    Units are Meters / Second

    Members are:
    - vx - x-component of the velocity vector
    - vy - y-component of the velocity vector
    - vz - z-component of the velocity vector
    """
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0


@dataclass
class Quaternion:
    """
    Rotation quaternion that represents the orientation of a body
    in free space.

    Units are Radians

    Members are:
    - w - relates the rotational magnitude of an orientation
    - x - similar to x coordinate in traditional coordinate system
    - y - similar to y coordinate in traditional coordinate system
    - z - similar to z coordinate in traditional coordinate system

    Reference:
    https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
    """
    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def length(self) -> float:
        return sqrt(pow(self.w, 2)
                    + pow(self.x, 2)
                    + pow(self.y, 2)
                    + pow(self.z, 2))
    
    def unitize(self) -> None:
        """
        Ensures that any quaternion is normalized to a unit quaternion,
        or more generally, to a quaternion that has a length of one.
        This is important when describing the orientation of a physical
        body by a quaternion.

        Divdes each comnponent of the quaternion by the length of the
        quaternion, return each component as a float.
        """
        length = self.length()
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length
        self.w = self.w / length


@dataclass
class MovementCommand():
    """
    AirSim requires a Movement command, which contains a number of
    different properties. In general, this movement command will be the
    next X, Y and Z positions of the UAV in the local NED coordiante
    frame, along with the orientation that the drone should be headed
    in, the speed at which the UAV should approach that target and the
    UAV ID of the message.

    ## Inputs:
    - position [PosVec3] X,Y,Z NED position in the local coordinate
                         frame. Initialzied as X=0, Y=0, Z=0,
                         Frame=Local
    - heading [float] Yaw angle of drone, with inital heading being 0.0
                      in Degrees
    - speed [float] Speed to travel in the direction of travel in meters
                    per second
    """
    position: PosVec3 = PosVec3()
    heading: float = 0.0 # degrees
    speed: float = 5.0 # meters / second