import time

import cv2

cap = cv2.VideoCapture('../video/test5.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")  # 加载级联分类器模型
face_cascade.load(r'../res/haarcascade_frontalface_alt2.xml')


def face_rect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将图片转化成灰度
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return frame


while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frame = face_rect(frame)
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    time.sleep(1/fps)

cap.release()
cv2.destroyAllWindows()
