from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2


kinect_ir = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared)
kinect_color = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)
depth_width, depth_height = kinect_ir.depth_frame_desc.Width, kinect_ir.depth_frame_desc.Height

def correction(img):
    a = 1.0
    b = 0.02
    img_1 = img[:,:50].copy()
    img_1 = cv2.resize(img_1,dsize = None,fx = a+b*1,fy = 1.0)
    img_2 = img[:,50:100].copy()
    img_2 = cv2.resize(img_2,dsize = None,fx = a+b*2,fy = 1.0)
    img_3 = img[:,100:150].copy()
    img_3 = cv2.resize(img_3,dsize = None,fx = a+b*3,fy = 1.0)
    img_4 = img[:,150:200].copy()
    img_4 = cv2.resize(img_4,dsize = None,fx = a+b*4,fy = 1.0)
    img_5 = img[:,200:250].copy()
    img_5 = cv2.resize(img_5,dsize = None,fx = a+b*5,fy = 1.0)
    img_6 = img[:,250:300].copy()
    img_6 = cv2.resize(img_6,dsize = None,fx = a+b*6,fy = 1.0)
    img_7 = img[:,300:350].copy()
    img_7 = cv2.resize(img_7,dsize = None,fx = a+b*7,fy = 1.0)
    img_8 = img[:,350:400].copy()
    img_8 = cv2.resize(img_8,dsize = None,fx = a+b*8,fy = 1.0)
    img_9 = img[:,400:450].copy()
    img_9 = cv2.resize(img_9,dsize = None,fx = a+b*9,fy = 1.0)
    img_10 = img[:,450:500].copy()
    img_10 = cv2.resize(img_10,dsize = None,fx = a+b*10,fy = 1.0)
    img_11 = img[:,500:].copy()
    img_11 = cv2.resize(img_11,dsize = None,fx = a+b*11,fy = 1.0)

    img_co = cv2.hconcat([img_1,img_2,img_3,img_4,img_5,img_6,img_7,img_8,img_9,img_10,img_11])
    img_co = img_co[:,0:512]

    return img_co

while True:
    # --- Getting frames and drawing
    if kinect_ir.has_new_infrared_frame() and kinect_color.has_new_color_frame():

        frame_ir = kinect_ir.get_last_infrared_frame()
        frame_ir = np.uint8(frame_ir.clip(1, 4080) / 16.)
        frame_ir = np.reshape(frame_ir, (depth_height, depth_width)).astype(np.uint8)
        #print(frame.shape)
        #cv2.cvtColor(frame_ir, cv2.COLOR_GRAY2BGR)
        ret,thresh1 = cv2.threshold(frame_ir,130,255,cv2.THRESH_BINARY)
        #thresh1 = cv2.resize(thresh1, dsize=None, fx=1.2, fy=1.0)
        #thresh1 = thresh1[:,0:512]
        #print(thresh1.shape)
        thresh1 = correction(thresh1)
        thresh1 = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2RGB)
        #print(thresh1.shape)
        #cv2.imshow('KINECT Video Stream1', thresh1)


    #if kinect_color.has_new_color_frame():
        frame_color = kinect_color.get_last_color_frame()
        frame_color = frame_color.reshape((1080, 1920,-1)).astype(np.uint8)
        scale = max(512 / frame_color.shape[1], 424 / frame_color.shape[0])
        frame_color = cv2.resize(frame_color, dsize=None,fx=scale,fy=scale)
        frame_color = frame_color[:,121:633]
        #print(frame.shape)
        frame_color = cv2.cvtColor(frame_color, cv2.COLOR_RGBA2RGB)
        #cv2.imshow('KINECT Video Stream2', frame_color)

        dst = cv2.bitwise_and(frame_color, thresh1)

        cv2.imshow('KINECT Video Stream', dst)


        frame_ir = None
        frame_color = None

    key = cv2.waitKey(1)
    if key == 27: break
