import cv2

from vision import position as pos
from vision import plotting as plot
from vision import navigation as navi
from vision import user_functions as userf
from vision import utils

cap = userf.initialize_CV()
#if Needed
while 1:
	coords , angle = userf.return_position(cap)
