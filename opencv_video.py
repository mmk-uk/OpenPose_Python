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

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    bodys = upperbody_cascade.detectMultiScale(gray)
    for x, y, w, h in bodys:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        body = frame[y: y + h, x: x + w]
        body_gray = gray[y: y + h, x: x + w]

        faces = face_cascade.detectMultiScale(body_gray)
        for x, y, w, h in faces:
            cv2.rectangle(body, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = body[y: y + h, x: x + w]
            face_gray = body_gray[y: y + h, x: x + w]

            eyes = eye_cascade.detectMultiScale(face_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)


    cv2.imshow('Raw Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
