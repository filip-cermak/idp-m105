"""Functionality for detecting robot position from a single frame"""

import cv2
import numpy as np
import time


def set_detector_params(by_color=False,
					    color=255,
					    by_area=True,
					    min_area=300,
					    max_area=600,
					    by_circularity=True,
					    min_circularity=0.7,
					    by_convexity=False,
					    min_convexity=0.5,
					    by_inertia=False,
					    min_inertia=0.1):
	""" """
	params = cv2.SimpleBlobDetector_Params()

	# color
	params.filterByColor = by_color
	params.blobColor = color

	# area
	params.filterByArea = by_area
	params.minArea = min_area # TODO get all blobs to correct size and tweak
	params.maxArea = max_area

	# circularity
	params.filterByCircularity = by_circularity
	params.minCircularity = min_circularity

	# convexity
	params.filterByConvexity = by_convexity
	params.minConvexity = min_convexity

	# inertia
	params.filterByInertia = by_inertia
	params.minInertiaRatio = min_inertia

	return params


def initialize_detector(params,
						print_result=True):
	""" """
	if cv2.__version__.startswith('2.'):
	    detector = cv2.SimpleBlobDetector(params)
	    if print_result:
	    	print('Different version of openCV - may have bugs')
	else:
	    detector = cv2.SimpleBlobDetector_create(params)
	    if print_result:
	    	print('Simple Blob Detector created')


	return detector


def crop_frame(frame,
			   x_min=160,
			   x_max=1500,
			   y_min=0,
			   y_max=1080):
	""" Hardcoded for Table 2 """
	cropped_frame = frame[y_min:y_max, x_min:x_max]

	return cropped_frame


def detect_red_blobs(frame,
					 detector,
					 lower_red_bgr=[0, 0, 150],
					 upper_red_bgr=[140,140,255],
					 blur_val=5,
					 thresh_min=150,
					 thresh_max=255):
	""" """
	lower_red = np.array(lower_red_bgr) # b, g, r
	upper_red = np.array(upper_red_bgr)

	mask = cv2.inRange(frame, lower_red, upper_red)

	res = cv2.bitwise_and(frame, frame, mask=mask)

	res = cv2.medianBlur(res, blur_val)

	_, res = cv2.threshold(res, thresh_min, thresh_max, cv2.THRESH_BINARY)

	keypoints = detector.detect(res)

	return keypoints


def draw_keypoints(frame,
				   keypoints,
				   color=(255,0,0)):
	""" """
	frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), color,
		cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	return frame_with_keypoints

def write_num_of_keypoints(frame,
						   keypoints,
						   position=(500, 30),
						   font=cv2.FONT_HERSHEY_SIMPLEX,
						   color=(0, 0, 255)): #TODO add other params
	"""In place write on frame"""
	printed_text = '{} red blob(s) detected.'.format(len(keypoints))

	frame_with_text = cv2.putText(frame, printed_text, position, font, 1, color, 2, cv2.LINE_AA)

	return frame_with_text

def get_coords_distance(coords_1,
						coords_2):
	""" """
	return np.linalg.norm(np.array(coords_2) - np.array(coords_1))


def get_robot_coords(keypoints,
					 back_blobs_dist=40,
					 back_blobs_dist_tol=10):
	""" back_blobs_dist - back_blobs_dist_tol has to be positive"""
	
	if len(keypoints) == 3:
		new_3_keypoints = [(keypoint.pt[0], keypoint.pt[1]) for keypoint in keypoints]
		# assert len is 3

		for blob_coords in new_3_keypoints:
			for blob_coords_2 in new_3_keypoints:
				
				coords_distance = get_coords_distance(blob_coords, blob_coords_2)

				if coords_distance > (back_blobs_dist - back_blobs_dist_tol) and coords_distance < (back_blobs_dist + back_blobs_dist_tol):
					back_blobs_coords = [blob_coords, blob_coords_2]
					front_blob_coords = [blob_coords_3 for blob_coords_3 in new_3_keypoints if (blob_coords_3 not in back_blobs_coords)]
					front_blob_coords = front_blob_coords[0]

					# TODO add checks
					# if robot coordinates are stored and can be used for later
					break

	# TODO add branch if more/less than 3 blobs are detected
	else:
		pass


	try:
		return back_blobs_coords, front_blob_coords
	except: # TODO
		 raise Exception('Robot coordinates not found')


def get_back_midpoint(back_blobs_coords):
	""" """
	back_midpoint = (int((back_blobs_coords[0][0] + back_blobs_coords[1][0])/2),
			int((back_blobs_coords[0][1] + back_blobs_coords[1][1])/2))

	return back_midpoint


def get_middle_midpoint(front_blob_coords,
						back_midpoint):
	""" """
	middle_midpoint = (int((back_midpoint[0] + front_blob_coords[0])/2),
			int((back_midpoint[1] + front_blob_coords[1])/2))

	return middle_midpoint


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
