import sys
import numpy as np
import cv2
import os
from sys import platform
import argparse
import time
import tkinter as tk
import threading
import hand_module as hm
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

root = tk.Tk()
root.title("認識結果")
root.geometry("600x600+1200+50")

rootFlag = True

canvas = tk.Canvas(root,width=600,height=600)
canvas.grid()

canvas.create_text(300,300,text='',font=('',350))

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

def adjust(img, alpha=1.0, beta=0.0):
    dst = alpha * img + beta
    return np.clip(dst,0,255).astype(np.uint8)

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

def display(root):
    global rootFlag
    root.mainloop()
    rootFlag = False

def openpose_demo(canvas):
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"
    params["hand"] = True

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    kinect_ir = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared | PyKinectV2.FrameSourceTypes_Depth)
    kinect_color = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)
    depth_width, depth_height = kinect_ir.depth_frame_desc.Width, kinect_ir.depth_frame_desc.Height

    before_form = []
    current_form = []
    counter = 0
    global rootFlag
    while(True):

        frame_ir = kinect_ir.get_last_infrared_frame()
        frame_ir = np.uint8(frame_ir.clip(1, 4080) / 16.)
        frame_ir = np.reshape(frame_ir, (depth_height, depth_width)).astype(np.uint8)
        ret,thresh1 = cv2.threshold(frame_ir,130,255,cv2.THRESH_BINARY)
        thresh1 = correction(thresh1)
        thresh1 = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2RGB)
        M = np.float32([[1,0,7],[0,1,0]])
        kernel = np.ones((5,5),np.uint8)
        thresh1 = cv2.dilate(thresh1,kernel,iterations = 1)
        thresh1 = cv2.warpAffine(thresh1,M,(512,424))

        frame_color = kinect_color.get_last_color_frame()
        frame_color = frame_color.reshape((1080, 1920,-1)).astype(np.uint8)
        scale = max(512 / frame_color.shape[1], 424 / frame_color.shape[0])
        frame_color = cv2.resize(frame_color, dsize=None,fx=scale,fy=scale)
        frame_color = frame_color[:,121:633]
        frame_color = cv2.cvtColor(frame_color, cv2.COLOR_RGBA2RGB)

        frame = cv2.bitwise_and(frame_color, thresh1)

        frame_ir = None
        frame_color = None

        # Process Image
        datum = op.Datum()
        imageToProcess = frame
        datum.cvInputData = imageToProcess

        opWrapper.emplaceAndPop([datum])

        cv2.namedWindow("OpenPose 1.5.0 - Tutorial Python API", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL) #ウィンドウサイズを可変に
        cv2.imshow("OpenPose 1.5.0 - Tutorial Python API", datum.cvOutputData)

        #print(datum.handKeypoints[1][0])
        try:
            right_hand,flag = hm.is_hand_recog(datum.handKeypoints[1][0])
        except Exception as e:
            continue
        #カメラの指定によっては「IndexError: too many indices for array」というエラーが出る

        if flag == True:
            current_form = hm.check_handform2(right_hand)
            print(hm.list_to_num(current_form))
            #print(current_form,counter)
            if current_form == before_form:   #1フレーム前の形と現在の形を比較する
                counter = counter + 1  #同じだったらカウントを１増やす
                if(counter == 2): #カウントが10になったら（10回連続して同じ形を認識したら）
                    canvas.delete("all")
                    n = hm.list_to_num(current_form) #手の形から番号を決定
                    try:
                        canvas.create_text(300,300,text=n,font=('',350))
                    except Exception as e:
                        break
            else:
                counter = 0 #違ったらカウントをリセットする
            before_form = current_form
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if rootFlag == False:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    th2 = threading.Thread(target=openpose_demo,args=(canvas,))
    th2.start()
    display(root)
