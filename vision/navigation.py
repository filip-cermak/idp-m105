""" Module provides navigation functionality for the robot"""
import cv2
import numpy as np


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def get_robot_direction(front_blob_coords,
					    back_midpoint,
					    front_dir_vector=[162, -5]): # perpendicular to start wall
	""" Angle in radians from perpendicular line from start wall """

	robot_direction_x = front_blob_coords[0] - back_midpoint[0]
	robot_direction_y = front_blob_coords[1] - back_midpoint[1]
	robot_direction = [robot_direction_x, robot_direction_y]

	return angle_between(robot_direction, front_dir_vector)
