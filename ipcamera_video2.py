import cv2

URL = "rtsp://admin:888888@192.168.10.101:10554/tcp/av0_0"
s_video = cv2.VideoCapture(URL)

while True:
  ret, img = s_video.read()
  cv2.imshow("Stream Video",img)
  key = cv2.waitKey(1) & 0xff
  if key == ord('q'):
      break
