from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2

kinect_ir = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared)
#kinect_color = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)

depth_width, depth_height = kinect_ir.depth_frame_desc.Width, kinect_ir.depth_frame_desc.Height
while True:
    if kinect_ir.has_new_infrared_frame():

        #ir image get
        frame_ir = kinect_ir.get_last_infrared_frame()
        #frame_ir = frame_ir.astype(np.uint16)
        frame_ir = np.uint8(frame_ir.clip(1, 4080) / 16.)
        frame_ir = np.reshape(frame_ir, (depth_width, depth_height)).astype(np.uint8)
        #frame_ir = cv2.cvtColor(frame_ir, cv2.COLOR_GRAY2BGR)
        cv2.imshow('KINECT Video Stream2', frame_ir)

        frame_ir = None

#    if kinect_color.has_new_color_frame():

        #color image get
    #    frame_color = kinect_color.get_last_color_frame()
    #    frame_color = frame_color.reshape((1080, 1920,-1)).astype(np.uint8)
    #    scale = max(512 / frame_color.shape[1], 424 / frame_color.shape[0])
    #    frame_color = cv2.resize(frame_color, dsize=None,fx=scale,fy=scale)
    #    frame_color = frame_color[:,121:633]
    #    frame_color = cv2.cvtColor(frame_color, cv2.COLOR_RGBA2RGB)
    #    cv2.imshow('KINECT Video Stream1', frame_color)

    #    frame_color = None


    key = cv2.waitKey(1)
    if key == 27: break
