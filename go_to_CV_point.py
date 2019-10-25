import cv2
import numpy as np

from vision import position as pos
from vision import plotting as plot
from vision import navigation as navi
from vision import user_functions as userf
from vision import utils

from wifi import UDP_connect as udp

cap = userf.initialize_CV()

#robot correctly rotated now
#initialize the motors
#stop when UDP stop package received from PC and robot close to the Point
coords , angle = userf.return_position(cap)
goal_coords = [300,300]
dist = numpy.linalg.norm(a-b)

dist *= K #need to calibrate

#send packet to go for a certain dist

angle_goal = 0
