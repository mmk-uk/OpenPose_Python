from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared)
depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height

while True:
    # --- Getting frames and drawing
    if kinect.has_new_infrared_frame():
        frame = kinect.get_last_infrared_frame()
        frame = frame.astype(np.uint16)
        frame = np.uint8(frame.clip(1, 4080) / 16.)
        frame = np.reshape(frame, (depth_height, depth_width))
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        #print(frame.shape)
        cv2.imshow('KINECT Video Stream', frame)
        frame = None

    key = cv2.waitKey(1)
    if key == 27: break
