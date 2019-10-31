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
        self.onoff = False
        self.channel = [1,2,4,5,6,7,8,9]
        self.now = 0
        self.vol = 10
        self.volcon = 0
        self.range = 0

        self.params = dict()
        self.params["model_folder"] = "../../../models/"
        self.params["hand"] = True

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(self.params)
        self.opWrapper.start()

        self.cap = cv2.VideoCapture(0) #0だったり1だったり
        self.cap.set(3,1920)
        self.cap.set(4,1080)

        self.before_form = []
        self.current_form = []
        self.counter = 0
        pyxel.init(60, 45)
        pyxel.run(self.update,self.draw)

    def update(self):

        ret,frame = self.cap.read()
        # Process Image
        datum = op.Datum()
        imageToProcess = frame
        datum.cvInputData = imageToProcess

        self.opWrapper.emplaceAndPop([datum])
        cv2.namedWindow("OpenPose 1.5.0 - Tutorial Python API", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL) #ウィンドウサイズを可変に
        cv2.imshow("OpenPose 1.5.0 - Tutorial Python API", datum.cvOutputData)


        right_hand,flag = hm.is_hand_recog(datum.handKeypoints[1][0])


        self.current_form = hm.check_handform2(right_hand)
        if self.current_form == self.before_form:   #1フレーム前の形と現在の形を比較する
            self.counter = self.counter + 1  #同じだったらカウントを１増やす
            if(self.counter == 5): #カウントが10になったら（10回連続して同じ形を認識したら）
                n = hm.list_to_num(self.current_form) #手の形から番号を決定
                print(n)
        else:
            self.counter = 0 #違ったらカウントをリセットする
        self.before_form = self.current_form

        if self.onoff:

            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.now = changechannel(self.now,1)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.now = changechannel(self.now,-1)
            if pyxel.btnr(pyxel.KEY_UP):
                pyxel.cls(channelToImage(self.channel[self.now]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[self.now]), 0)
                self.vol = volumeChange(self.vol,1)
                self.volcon = 50


            if pyxel.btnr(pyxel.KEY_DOWN):
                pyxel.cls(channelToImage(self.channel[self.now]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[self.now]), 0)
                self.vol = volumeChange(self.vol,-1)
                self.volcon = 50

        if pyxel.btnr(pyxel.KEY_O) and self.onoff==True:
            self.onoff = False
            self.range = int(pyxel.height/2)
            self.volcon = 0

        if pyxel.btnr(pyxel.KEY_I) and self.onoff==False:
            self.onoff = True
            self.range = 0
            print(self.onoff)


    def draw(self):

        if self.onoff:
            pyxel.cls(channelToImage(self.channel[self.now]))
            if self.range < int(pyxel.height/2):
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range += 5
            pyxel.text(5, 5, str(self.channel[self.now]), 0)

        else:
            pyxel.cls(0)
            if 0 < self.range:
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range -= 5


        if self.volcon > 0:
            pyxel.text(int(pyxel.width/2), int(pyxel.height)-5, "vol:{}".format(self.vol), 0)
            self.volcon -= 1

TV()
