import sys
import numpy as np
import cv2
import os
from sys import platform
import argparse
import time
import hand_module as hm


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

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"
params["hand"] = True

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

cap = cv2.VideoCapture(0)

before_form = []
current_form = []
counter = 0
while(True):
    ret,frame = cap.read()

    # Process Image
    datum = op.Datum()
    imageToProcess = frame
    datum.cvInputData = imageToProcess

    opWrapper.emplaceAndPop([datum])

    cv2.imshow("OpenPose 1.5.0 - Tutorial Python API", datum.cvOutputData)

    #print(datum.handKeypoints[1][0])

    right_hand,flag = hm.is_hand_recog(datum.handKeypoints[1][0])
    if flag == True:
        current_form = hm.check_handform2(right_hand)
        #print(current_form,counter)
        if current_form == before_form:
            counter = counter + 1
            if(counter == 10):
                print(hm.list_to_num(current_form))
        else:
            counter = 0
        before_form = current_form
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
