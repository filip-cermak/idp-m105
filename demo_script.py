""" Demonstration script of vision for IDP robot"""

import cv2
from vision import position as pos
from vision import plotting as plot


camera_num = 1

params = pos.set_detector_params()

detector = pos.initialize_detector(params)

cap = cv2.VideoCapture(camera_num)

while True:
	ret, frame = cap.read()

	frame = pos.crop_frame(frame)

	keypoints = pos.detect_red_blobs(frame, detector)

	frame = pos.draw_keypoints(frame, keypoints)

	fin_frame = pos.write_num_of_keypoints(frame, keypoints)

	try:
		back_blobs_coords, front_blob_coords = pos.get_robot_coords(keypoints)
		has_robot_coords = True
	except Exception: # TODO
		has_robot_coords = False

	if has_robot_coords:

		back_midpoint = pos.get_back_midpoint(back_blobs_coords)
		
		middle_midpoint = pos.get_middle_midpoint(back_midpoint, front_blob_coords)
		
		robots_angle_to_front = pos.get_robot_direction(front_blob_coords, back_midpoint)

		plot.draw_midpoint(fin_frame, middle_midpoint)

		# plot.draw robot arrow

		# TODO next

	else:
		pass

	cv2.namedWindow('Table 2',cv2.WINDOW_NORMAL)

	cv2.resizeWindow('Table 2', (1280,720))

	cv2.imshow('Table 2', fin_frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
