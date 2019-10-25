from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)

while True:
    # --- Getting frames and drawing
    if kinect.has_new_color_frame():
        frame = kinect.get_last_color_frame()
        frame = frame.reshape((1080, 1920,-1)).astype(np.uint8)
        scale = max(512 / frame.shape[1], 424 / frame.shape[0])
        frame = cv2.resize(frame, dsize=None,fx=scale,fy=scale)
        frame = frame[:,121:633]
        #print(frame.shape)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        cv2.imshow('KINECT Video Stream', frame)
        frame = None


    key = cv2.waitKey(1)
    if key == 27: break
