"""Functionality for plotting on a single frame"""

import cv2
import numpy as np


def draw_midpoint(frame,
				  middle_midpoint,
				  size=10,
				  color=(255, 0, 255)):
	""" """

	frame = cv2.circle(frame, middle_midpoint, size, color, -1)


def draw_robot_arrow(frame,
					 back_midpoint,
					 front_blob_coords,
					 size=3,
					 color=(255, 0, 0)):
	""" """
	
	frame = cv2.arrowedLine(frame, back_midpoint, (int(front_blob_coords[0]), int(front_blob_coords[1])), color, size)
