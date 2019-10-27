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
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

root = tk.Tk()
root.title("認識結果")
root.geometry("600x600+1200+50")

rootFlag = True

canvas = tk.Canvas(root,width=600,height=600)
canvas.grid()

canvas.create_text(300,300,text='',font=('',350))

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

apikey = "v3mO8ahYZLOw7_lWpAPX6XZ3xvUcAgXQmU_HKi8-SEg.Wfzp5gZGCqBYoV8aUIc7b7p5AEBoLHO350a6FSQgePA"

#Get JSON
headers = {
  'accept': 'application/json',
  'Authorization': 'Bearer ' + apikey ,
}

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

    cap = cv2.VideoCapture(0) #0だったり1だったり
    #cap.set(3,1280)
    #cap.set(4,960)
    cap.set(3,1920)
    cap.set(4,1080)

    before_form = []
    current_form = []
    counter = 0
    global rootFlag
    while(True):
        ret,frame = cap.read()
        #cv2.imshow('Raw Frame', frame)
        #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)

        #frame = adjust(frame,alpha=1.0,beta=-25.0)

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
            if current_form == before_form:   #1フレーム前の形と現在の形を比較する
                counter = counter + 1  #同じだったらカウントを１増やす
                if(counter == 5): #カウントが10になったら（10回連続して同じ形を認識したら）
                    canvas.delete("all")
                    n = hm.list_to_num(current_form) #手の形から番号を決定
                    #if n == '5':
                    #    response = requests.post('https://api.nature.global/1/signals/c0035911-6e5d-43c5-a965-c11dcebcf924/send', headers=headers, verify=False)
                    #if n == '4':
                    #    response = requests.post('https://api.nature.global/1/signals/00db0c08-6677-410a-bb65-4f2edc7d47c8/send', headers=headers, verify=False)
                    #    response = requests.post('https://api.nature.global/1/signals/00db0c08-6677-410a-bb65-4f2edc7d47c8/send', headers=headers, verify=False)
                    #if n == '3':
                    #    response = requests.post('https://api.nature.global/1/signals/9ca9ac8e-8739-4dad-9e75-bf1f8a93b597/send', headers=headers, verify=False)
                    #    response = requests.post('https://api.nature.global/1/signals/9ca9ac8e-8739-4dad-9e75-bf1f8a93b597/send', headers=headers, verify=False)
                    try:
                        canvas.create_text(300,300,text=n,font=('',350))
                    except Exception as e:
                        break
            else:
                counter = 0 #違ったらカウントをリセットする
                try:
                    canvas.delete("all")
                except Exception as e:
                    break

            before_form = current_form
        else:
            canvas.delete("all")

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
