import numpy as np
import math

#手を認識しているかどうかを調べる関数（＋右手のキーポイント座標の配列を返す）
def is_hand_recog(handdata):
    right_hand = []
    flag = True
    for point in handdata:
        right_hand.append((point[0],point[1]))
        if point[0]==0. and point[1]==0. and point[2]==0.:
            flag = False
    return right_hand,flag


#３点からなる角度を求める関数
def joint_angle(A,B,C):
    try:
        a = np.radians(np.array(A))
        b = np.radians(np.array(B))
        c = np.radians(np.array(C))
        avec = a - b
        cvec = c - b
        lat = b[0]
        avec[1] *= math.cos(lat)
        cvec[1] *= math.cos(lat)
        return np.degrees(math.acos(np.dot(avec, cvec) / (np.linalg.norm(avec) * np.linalg.norm(cvec))))
    except Exception as e:
        return 0

#２点間の距離を求める関数
def distance(A,B):
    a = np.array(A)
    b = np.array(B)
    #a = np.array([A[0],A[1]])
    #b = np.array([B[0],B[1]])
    u = b - a
    return np.linalg.norm(u)

def check_handform(right_hand):
    finger = []
    finger.append(joint_angle(right_hand[2],right_hand[3],right_hand[4]))
    finger.append(joint_angle(right_hand[5],right_hand[6],right_hand[7]))
    finger.append(joint_angle(right_hand[9],right_hand[10],right_hand[11]))
    finger.append(joint_angle(right_hand[13],right_hand[14],right_hand[15]))
    finger.append(joint_angle(right_hand[17],right_hand[18],right_hand[19]))

    handform = []
    for i in range(5):
        if finger[i]<135:
            handform.append(0)
        else:
            handform.append(1)

    return handform

def check_handform2(rh):
    handform = []
    #親指
    if distance(rh[5],rh[17])*1.2 > distance(rh[4],rh[17]):
        handform.append(0)
    else:
        handform.append(1)
    #人差し指
    if distance(rh[0],rh[5])*1.2 > distance(rh[0],rh[8]):
        handform.append(0)
    else:
        handform.append(1)
    #中指
    if distance(rh[0],rh[9])*1.2 > distance(rh[0],rh[12]):
        handform.append(0)
    else:
        handform.append(1)
    #薬指
    if distance(rh[0],rh[13])*1.2> distance(rh[0],rh[16]):
        handform.append(0)
    else:
        handform.append(1)
    #小指
    if distance(rh[0],rh[18])*1.1 > distance(rh[0],rh[19]):
        handform.append(0)
    else:
        handform.append(1)

    return handform

def list_to_num(ls):
    if ls == [0,0,0,0,0]:
        return '0'
    elif ls == [0,1,0,0,0]:
        return '1'
    elif ls == [0,1,1,0,0]:
        return '2'
    elif ls == [0,1,1,1,0]:
        return '3'
    elif ls == [0,1,1,1,1]:
        return '4'
    elif ls == [1,1,1,1,1]:
        return '5'
    else:
        return '*'
