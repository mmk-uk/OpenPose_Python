import cv2.cv2 as cv2

upperbody_cascade_path = 'haarcascade_upperbody.xml'
face_cascade_path = 'haarcascade_frontalface_default.xml'
eye_cascade_path = 'haarcascade_eye.xml'

upperbody_cascade = cv2.CascadeClassifier(upperbody_cascade_path)
face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

cap = cv2.VideoCapture(0) # 配信のURLを指定
cap.set(3,1280)
cap.set(4,960)

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    print(frame.shape)
    cv2.imshow('Raw Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
