import cv2
from vision import position as pos
from vision import plotting as plot
from vision import navigation as navi
from vision import utils

def initialize_CV():
     camera_num = 1
     window_res = (1280,720)
     # Framerate parameters

     params = pos.set_detector_params()
     detector = pos.initialize_detector(params)
     cap = cv2.VideoCapture(camera_num)

     #Comment this for Mac
     cap.set(3,1920)
     cap.set(4, 1080)

     return cap

def return_position(cap):
    ret, frame = cap.read()
    frame = pos.crop_frame(frame)
    keypoints = pos.detect_red_blobs(frame, detector)
    plot.draw_keypoints(frame, keypoints)
    plot.write_num_of_keypoints(frame, keypoints)

    while(1): #TODO
        try:
            back_blobs_coords, front_blob_coords = pos.get_robot_coords(keypoints)
            has_robot_coords = True
            break

        except Exception as e: # TODO
        	has_robot_coords = False

    # Angle
    robots_angle_to_front = navi.get_robot_direction(front_blob_coords, back_midpoint)

    return front_blob_coords, robots_angle_to_front
