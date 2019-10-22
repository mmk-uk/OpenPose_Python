import cv2

upperbody_cascade_path = 'haarcascade_upperbody.xml'
face_cascade_path = 'haarcascade_frontalface_default.xml'
eye_cascade_path = 'haarcascade_eye.xml'

upperbody_cascade = cv2.CascadeClassifier(upperbody_cascade_path)
face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

src = cv2.imread("../../../examples/media/COCO_val2014_000000000459.jpg")
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

bodys = upperbody_cascade.detectMultiScale(src_gray)
for x, y, w, h in bodys:
    cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 2)
    body = src[y: y + h, x: x + w]
    body_gray = src_gray[y: y + h, x: x + w]

    faces = face_cascade.detectMultiScale(body_gray)
    for x, y, w, h in faces:
        cv2.rectangle(body, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = src[y: y + h, x: x + w]
        face_gray = src_gray[y: y + h, x: x + w]

        eyes = eye_cascade.detectMultiScale(face_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)




cv2.imshow('data/dst/opencv_face_detect_rectangle.jpg', src)
cv2.waitKey(0)
cv2.destroyAllWindows()
