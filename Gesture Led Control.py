import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from cvzone.SerialModule import SerialObject
################################
wCam, hCam = 640, 480
################################
arduino = SerialObject()
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()

minbright = 0
maxbright = 255
bright = 0
brightbar = 400
brightper = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)
        # Hand range 50 - 300
        # Bright Range 0 - 255

        bright = np.interp(length, [50, 300], [minbright , maxbright])
        brightbar = np.interp(length, [50, 300], [400, 150])
        brightper = np.interp(length, [50, 300], [0, 100])
        print(int(length), int(bright))
        arduino.sendData([int(bright)])
       
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(brightbar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(brightper)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
