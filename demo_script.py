""" Demonstration script of vision for IDP robot, set for Table 2"""

import cv2
from vision import position as pos
from vision import plotting as plot
from vision import navigation as navi
from vision import utils


# Initialization parameters
camera_num = 1

window_res = (1280,720)

# Framerate parameters
has_already_started = False
start_time = 0
frame_counter = 0
frame_rate = 0

params = pos.set_detector_params()

detector = pos.initialize_detector(params)

cap = cv2.VideoCapture(camera_num)


# Main camera loop
while True:
	ret, frame = cap.read()

	frame = pos.crop_frame(frame)

	keypoints = pos.detect_red_blobs(frame, detector)

	plot.draw_keypoints(frame, keypoints)

	plot.write_num_of_keypoints(frame, keypoints)

	# Try to detect robot coordinates from detected keypoints (red blobs)
	try:
		back_blobs_coords, front_blob_coords = pos.get_robot_coords(keypoints)
		has_robot_coords = True
	except Exception as e: # TODO
		has_robot_coords = False


	# If robot's coordinates are detected
	if has_robot_coords:

		# Points
		back_midpoint = pos.get_back_midpoint(back_blobs_coords)
		
		middle_midpoint = pos.get_middle_midpoint(back_midpoint, front_blob_coords)
		
		# Angle
		robots_angle_to_front = navi.get_robot_direction(front_blob_coords, back_midpoint)

		# Distances from walls/ safe area line
		# Currently using front point of the robot
		safe_area_line_dist = navi.get_safe_area_line_dist(front_blob_coords)

		left_wall_line_dist = navi.get_left_wall_line_dist(front_blob_coords)

		right_wall_line_dist = navi.get_right_wall_line_dist(front_blob_coords)
		
		back_wall_line_dist = navi.get_back_wall_line_dist(front_blob_coords)

		# Whether in mine area or not
		in_mine_area = navi.is_in_mine_area(safe_area_line_dist)

		# Can set thresholds as second argument
		close_to_safe_area = navi.is_close_to_safe_area_line(safe_area_line_dist)

		close_to_left_wall = navi.is_close_to_left_wall_line(left_wall_line_dist)

		close_to_right_wall = navi.is_close_to_right_wall_line(right_wall_line_dist)

		close_to_back_wall = navi.is_close_to_back_wall_line(back_wall_line_dist)


		# Robot plotting
		plot.draw_midpoint(frame, middle_midpoint)

		plot.draw_robot_arrow(frame, back_midpoint, front_blob_coords)

	# Branch if robots position not detected
	else:
		pass


	# Framerate - works only if inside while loop for opecv camera feed
	has_already_started, start_time, frame_counter, frame_rate = utils.get_framerate(
		has_already_started, start_time, frame_counter, frame_rate)


	# Plotting
	# Hardcoded areas
	plot.plot_mine_field(frame)

	plot.plot_red_area(frame)

	plot.plot_green_area(frame)

	plot.plot_start_area(frame)

	# Framerate
	plot.write_framerate(frame, frame_rate)


	# Displaying window
	cv2.namedWindow('Table 2',cv2.WINDOW_NORMAL)

	cv2.resizeWindow('Table 2', window_res)

	cv2.imshow('Table 2', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
