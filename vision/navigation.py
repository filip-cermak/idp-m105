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


def get_dist_from_line(point_coords,
                       first_line_coords,
                       second_line_coords):
    """ Computes shortest distance between a point and line
    defined by two points, expects coords as lists of x,y"""

    first_line_coords = np.array(first_line_coords)
    second_line_coords = np.array(second_line_coords)

    dist = np.cross(second_line_coords-first_line_coords,
            point_coords-first_line_coords)/np.linalg.norm(
            second_line_coords-first_line_coords)

    return dist


def get_safe_area_line_dist(robot_blob_coords,
                            first_line_coords=[316, 1080],
                            second_line_coords=[276, 0]):
    """ Computes shortest distance from safe area line"""

    return get_dist_from_line(robot_blob_coords,
                              first_line_coords,
                              second_line_coords)


# left wall is top wall on camera, left when considering starting robot position
def get_left_wall_line_dist(robot_blob_coords,
                            first_line_coords=[276, 0],
                            second_line_coords=[1340, 0]):
    """ Computes shortest distance from left wall line"""

    return get_dist_from_line(robot_blob_coords,
                              first_line_coords,
                              second_line_coords)


def get_right_wall_line_dist(robot_blob_coords,
                            first_line_coords=[1340, 1080],
                            second_line_coords=[316, 1080]):
    """ Computes shortest distance from right wall line"""

    return get_dist_from_line(robot_blob_coords,
                              first_line_coords,
                              second_line_coords)


def get_back_wall_line_dist(robot_blob_coords,
                            first_line_coords=[1340, 0],
                            second_line_coords=[1340, 1080]):
    """ Computes shortest distance from back wall line"""

    return get_dist_from_line(robot_blob_coords,
                              first_line_coords,
                              second_line_coords)


def is_in_mine_area(safe_area_line_dist):
    """ Determines if robot in mine area"""
    if safe_area_line_dist > 0:
        return True
    else:
        return False


def is_dist_under_thresh(dist,
                         thresh):
    """ Determines whether distance is under threshold"""
    if abs(dist) < thresh:
        return True
    else:
        return False


def is_close_to_safe_area_line(line_dist,
                               line_dist_lim=40):
    """ Returns True/False based on whether under limit from safe_area """
    return is_dist_under_thresh(line_dist,
                                line_dist_lim)


def is_close_to_left_wall_line(line_dist,
                               line_dist_lim=70):
    """ Returns True/False based on whether under limit from safe_area """
    return is_dist_under_thresh(line_dist,
                                line_dist_lim)


def is_close_to_right_wall_line(line_dist,
                                line_dist_lim=40):
    """ Returns True/False based on whether under limit from safe_area """
    return is_dist_under_thresh(line_dist,
                                line_dist_lim)


def is_close_to_back_wall_line(line_dist,
                                line_dist_lim=90):
    """ Returns True/False based on whether under limit from safe_area """
    return is_dist_under_thresh(line_dist,
                                line_dist_lim)
