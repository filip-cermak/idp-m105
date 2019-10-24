"""Functionality for plotting on a single frame"""

import cv2
import numpy as np


def draw_midpoint(frame,
				  middle_midpoint,
				  size=10,
				  color=(255, 0, 255)):
	""" Draws a circle in the middle of the robot given frame and
	coordinates of middle midpoint."""

	frame = cv2.circle(frame, middle_midpoint, size, color, -1)


def draw_robot_arrow(frame,
					 back_midpoint,
					 front_blob_coords,
					 size=3,
					 color=(255, 0, 0)):
	""" Draws an arrow from back midpoint to front blob coordinates
	on the robot. """
	
	frame = cv2.arrowedLine(frame, back_midpoint, 
		(int(front_blob_coords[0]), int(front_blob_coords[1])), color, size)


def plot_area(frame,
			  left_up_coords,
			  left_down_coords,
			  right_down_coords,
			  right_up_coords,
			  color,
			  width=4):
	""" Plots a polygon on the frame given coordinates of its four vertices.
	All coordinates need to be lists of x, y coordinates"""
	area_coords = np.array([left_up_coords, left_down_coords,
		right_down_coords, right_up_coords])

	frame =  cv2.polylines(frame, [area_coords], True, color, width)


def plot_mine_field(frame,
				    left_up_coords=[276, 0],
				    left_down_coords=[316, 1080],
				    right_down_coords=[1325, 1080],
				    right_up_coords=[1303, 0],
				    color=(0, 200, 200),
				    width=4):
	""" Plots mine field given its coordinates, default coordinates hardcoded in."""

	frame = plot_area(frame,
					  left_up_coords,
					  left_down_coords,
					  right_down_coords,
					  right_up_coords,
					  color,
					  width)


def plot_red_area(frame,
			      left_up_coords=[6, 0],
			      left_down_coords=[6, 147],
			      right_down_coords=[162, 140],
			      right_up_coords=[160, 0],
			      color=(100, 255, 100),
			      width=4):
	""" Plots red area given its coordinates, default coordinates hardcoded in."""

	frame = plot_area(frame,
					  left_up_coords,
					  left_down_coords,
					  right_down_coords,
					  right_up_coords,
					  color,
					  width)


def plot_green_area(frame,
			        left_up_coords=[8, 323],
			        left_down_coords=[11, 485],
			        right_down_coords=[173, 480],
			        right_up_coords=[168, 319],
			        color=(100, 100, 255),
			        width=4):
	""" Plots green area given its coordinates, default coordinates hardcoded in."""

	frame = plot_area(frame,
					  left_up_coords,
					  left_down_coords,
					  right_down_coords,
					  right_up_coords,
					  color,
					  width)


def plot_start_area(frame,
			        left_up_coords=[101, 1051],
			        left_down_coords=[101, 1080],
			        right_down_coords=[208, 1080],
			        right_up_coords=[206, 1051],
			        color=(100, 100, 255),
			        width=4):
	""" Plots green area given its coordinates, default coordinates hardcoded in."""

	frame = plot_area(frame,
					  left_up_coords,
					  left_down_coords,
					  right_down_coords,
					  right_up_coords,
					  color,
					  width)
