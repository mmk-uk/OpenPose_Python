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
import pyxel

root = tk.Tk()
root.title("認識結果")
root.geometry("600x600+1200+50")

onoff = False
now = 0
vol = 10


def changechannel(now,x):
    if x == 1:
        now+=1
    if x == -1:
        now-=1
    return now%8


def channelToImage(c):
    if c == 1:
        return 8
    if c == 2:
        return 3
    if c == 3:
        return 8
    if c == 4:
        return 9
    if c == 5:
        return 14
    if c == 6:
        return 12
    if c == 7:
        return 10
    if c == 8:
        return 6
    if c == 9:
        return 2
def volumeChange(vol,x):
    if x == 1:
        if vol<30:
            vol += 1

    if x == -1:
        if 0<vol:
            vol -= 1

    return vol

class TV:
    def __init__(self):
        self.channel = [1,2,4,5,6,7,8,9]
        self.volcon = 0
        self.range = 0
        pyxel.init(60, 45)
        pyxel.run(self.update,self.draw)

    def update(self):
        global onoff
        global now
        global vol

        if onoff:

            if pyxel.btnr(pyxel.KEY_RIGHT):
                now = changechannel(now,1)
            if pyxel.btnr(pyxel.KEY_LEFT):
                now = changechannel(now,-1)
            if pyxel.btnr(pyxel.KEY_UP):
                pyxel.cls(channelToImage(self.channel[now]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[now]), 0)
                vol = volumeChange(vol,1)
                self.volcon = 50


            if pyxel.btnr(pyxel.KEY_DOWN):
                pyxel.cls(channelToImage(self.channel[now]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[now]), 0)
                vol = volumeChange(vol,-1)
                self.volcon = 50

        if pyxel.btnr(pyxel.KEY_O) and onoff==True:
            onoff = False
            self.range = int(pyxel.height/2)
            self.volcon = 0

        if pyxel.btnr(pyxel.KEY_I) and onoff==False:
            onoff = True
            self.range = 0
            print(onoff)


    def draw(self):
        global onoff
        global now
        global vol

        if onoff:
            pyxel.cls(channelToImage(self.channel[now]))
            if self.range < int(pyxel.height/2):
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range += 5
            pyxel.text(5, 5, str(self.channel[now]), 0)

        else:
            pyxel.cls(0)
            if 0 < self.range:
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range -= 5


        if self.volcon > 0:
            pyxel.text(int(pyxel.width/2), int(pyxel.height)-5, "vol:{}".format(vol), 0)
            self.volcon -= 1

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


def openpose_demo():
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
            #print(current_form)
            if current_form == before_form:   #1フレーム前の形と現在の形を比較する
                counter = counter + 1  #同じだったらカウントを１増やす
                if(counter == 5): #カウントが10になったら（10回連続して同じ形を認識したら）
                    n = hm.list_to_num(current_form) #手の形から番号を決定
                    if n == '5':
                        global onoff
                        if onoff:
                            onoff = False
                        else:
                            onoff = True
                    if n == '4':
                        pass
                    if n == '3':
                        pass

            else:
                counter = 0 #違ったらカウントをリセットする
            before_form = current_form
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    th2 = threading.Thread(target=openpose_demo)
    th2.start()
    TV()
