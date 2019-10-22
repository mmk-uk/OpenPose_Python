import cv2.cv2 as cv2

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

upperbody_cascade_path = 'haarcascade_upperbody.xml'

upperbody_cascade = cv2.CascadeClassifier(upperbody_cascade_path)

cap = cv2.VideoCapture(0) # 配信のURLを指定
cap.set(3,1280)
cap.set(4,960)

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    bodys = upperbody_cascade.detectMultiScale(gray,minNeighbors=3,minSize=(100,100))
    max_x,max_y,max_h,max_w = max_body_select(bodys)
    #if max_h < 200:
    #    continue
    try:
        frame2 = frame[max_y - 20: max_y + max_h + 20, max_x + 20: max_x + max_w + 20]

        print(type(frame2))

        cv2.imshow('Raw Frame', frame2)
    except Exception as e:
        continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
