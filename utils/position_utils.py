from utils.data_classes import PosVec3


def position_to_list(position_vector,
                     starting_position: PosVec3 = PosVec3(),
                     frame="local") -> PosVec3:
    """
    Given a vector from AirSim, generate a List to iterate
    through.

    Inputs:
    - position_vector [AirSim Vector3] the x,y,z position vector

    Outputs:
    List of x,y,z position
    """
    return PosVec3(X=position_vector.x_val,
                   Y=position_vector.y_val,
                   Z=position_vector.z_val,
                   frame=frame)