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

def scale_box(img,width,height):
    scale = max(width / img.shape[1], height / img.shape[0])
    return cv2.resize(img,dsize=None,fx=scale,fy=scale)

def max_body_select(bodys):
    max_x = 0.0
    max_y = 0.0
    max_h = 0.0
    max_w = 0.0
    for x, y, w, h in bodys:
        if max_h+max_w < w+h:
            max_x = x
            max_y = y
            max_h = h
            max_w = w
    return int(max_x),int(max_y),int(max_h),int(max_w)

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

    upperbody_cascade_path = 'haarcascade_upperbody.xml'
    upperbody_cascade = cv2.CascadeClassifier(upperbody_cascade_path)
    cap = cv2.VideoCapture(0) #0だったり1だったり

    before_form = []
    current_form = []
    counter = 0
    global rootFlag
    while(True):
        ret,frame = cap.read()

        frame = adjust(frame,alpha=1.0,beta=-25.0)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        bodys = upperbody_cascade.detectMultiScale(gray,minNeighbors=3,minSize=(100,100))
        max_x,max_y,max_h,max_w = max_body_select(bodys)
        print(max_x,max_y,max_h,max_w)

        #if max_h < 200:
        #    continue
        try:
            frame2 = frame[max_y - 20: max_y + max_h + 20, max_x + 20: max_x + max_w + 20]
            #frame2 = scale_box(frame,640,480)
            cv2.imshow('Raw Frame', frame2)
            # Process Image
            datum = op.Datum()
            imageToProcess = frame2
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

        except Exception as e:
            continue


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
