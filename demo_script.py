""" Demonstration script of vision for IDP robot"""

import cv2
from vision import position as pos
from vision import plotting as plot
from vision import navigation as navi


# Initialization parameters
camera_num = 1

window_res = (1280,720)

params = pos.set_detector_params()

detector = pos.initialize_detector(params)

cap = cv2.VideoCapture(camera_num)


# Main camera loop
while True:
	ret, frame = cap.read()

	frame = pos.crop_frame(frame)

	keypoints = pos.detect_red_blobs(frame, detector)

	frame = pos.draw_keypoints(frame, keypoints)

	fin_frame = pos.write_num_of_keypoints(frame, keypoints)

	# Try to detect robot coordinates from detected keypoints (red blobs)
	try:
		back_blobs_coords, front_blob_coords = pos.get_robot_coords(keypoints)
		has_robot_coords = True
	except Exception: # TODO
		has_robot_coords = False


	# If robot's coordinates are detected
	if has_robot_coords:

		back_midpoint = pos.get_back_midpoint(back_blobs_coords)
		
		middle_midpoint = pos.get_middle_midpoint(back_midpoint, front_blob_coords)
		
		robots_angle_to_front = navi.get_robot_direction(front_blob_coords, back_midpoint)

		# Robot plotting
		plot.draw_midpoint(fin_frame, middle_midpoint)

		plot.draw_robot_arrow(fin_frame, back_midpoint, front_blob_coords)

	else:
		pass


	# Plotting
	# Hardcoded areas
	plot.plot_mine_field(fin_frame)

	plot.plot_red_area(fin_frame)

	plot.plot_green_area(fin_frame)

	plot.plot_start_area(fin_frame)


	# Displaying window
	cv2.namedWindow('Table 2',cv2.WINDOW_NORMAL)

	cv2.resizeWindow('Table 2', window_res)

	cv2.imshow('Table 2', fin_frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
