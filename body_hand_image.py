import sys
import cv2
import os
from sys import platform
import argparse
import time
import hand_module as hm

face_cascade_path = 'haarcascade_frontalface_default.xml'
eye_cascade_path = 'haarcascade_eye.xml'

face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

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

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default="../../../examples/media/IMG_9644.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"
params["hand"] = True

# Add others in path?
for i in range(0, len(args[1])):
    curr_item = args[1][i]
    if i != len(args[1])-1: next_item = args[1][i+1]
    else: next_item = "1"
    if "--" in curr_item and "--" in next_item:
        key = curr_item.replace('-','')
        if key not in params:  params[key] = "1"
    elif "--" in curr_item and "--" not in next_item:
        key = curr_item.replace('-','')
        if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()


try:
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read image and face rectangle locations
    imageToProcess = cv2.imread(args[0].image_path)
    # Create new datum
    datum = op.Datum()
    datum.cvInputData = imageToProcess

    # Process and display image
    opWrapper.emplaceAndPop([datum])
    #print(type(datum.poseKeypoints))  #<class 'numpy.ndarray'>
    print("Body keypoints: \n")
    print(datum.poseKeypoints)
    #頭部の座標を取得
    head_x = int(datum.poseKeypoints[0][0][0])
    head_y = int(datum.poseKeypoints[0][0][1])
    print(head_x,head_y)
    #for person in datum.poseKeypoints:
        #for keypoint in person:
            #print("{0}\t{1}\t{2}\n".format(keypoint[0],keypoint[1],keypoint[2]))
    #print("Left hand keypoints: \n")
    #print(datum.handKeypoints[0])
    print("Right hand keypoints: \n")
    right_hand = []
    for point in datum.handKeypoints[1][0]:
        right_hand.append((point[0],point[1]))
    #print(right_hand)
    print(hm.check_handform(right_hand))
    cv2.imshow("OpenPose 1.5.0 - Tutorial Python API", datum.cvOutputData)

    resultimage = imageToProcess

    src_gray = cv2.cvtColor(resultimage, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(src_gray)

    for x, y, w, h in faces:
        cv2.rectangle(resultimage, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = resultimage[y: y + h, x: x + w]
        face_gray = src_gray[y: y + h, x: x + w]
        eyes = eye_cascade.detectMultiScale(face_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    cv2.imwrite('data/dst/opencv_face_detect_rectangle.jpg', resultimage)

    cv2.waitKey(0)
except Exception as e:
    # print(e)
    sys.exit(-1)
