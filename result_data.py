import json
import numpy as np
import math

#ファイルの読み込み
json_file = open("output/IMG_8517_keypoints.json","r")
#json形式での読み込み
json_data = json.load(json_file)

#jsonデータの表示
#print(json.dumps(json_data, indent=2))

#右手のデータ
#print(json.dumps(json_data["people"][0]["hand_right_keypoints_2d"], indent=2))

#右手のデータ（リスト）
right_hand_data = json_data["people"][0]["hand_right_keypoints_2d"]

right_hand_x = []
right_hand_y = []
for i,c in zip(right_hand_data,range(63)):
    if c%3==0:
        right_hand_x.append(i)
    elif c%3==1:
        right_hand_y.append(i)

right_hand = []
for x,y in zip(right_hand_x,right_hand_y):
    right_hand.append((x,y))

#３点からなる角度を求める関数
def joint_angle(A,B,C):
    a = np.radians(np.array(A))
    b = np.radians(np.array(B))
    c = np.radians(np.array(C))
    avec = a - b
    cvec = c - b
    lat = b[0]
    avec[1] *= math.cos(lat)
    cvec[1] *= math.cos(lat)
    return np.degrees(math.acos(np.dot(avec, cvec) / (np.linalg.norm(avec) * np.linalg.norm(cvec))))


def check_handform(right_hand):
    finger = []
    finger.append(joint_angle(right_hand[2],right_hand[3],right_hand[4]))
    finger.append(joint_angle(right_hand[5],right_hand[6],right_hand[7]))
    finger.append(joint_angle(right_hand[9],right_hand[10],right_hand[11]))
    finger.append(joint_angle(right_hand[13],right_hand[14],right_hand[15]))
    finger.append(joint_angle(right_hand[17],right_hand[18],right_hand[19]))

    handform = []
    for i in range(5):
        if finger[i]<90:
            handform.append(0)
        else:
            handform.append(1)
    return handform



print(check_handform(right_hand))
