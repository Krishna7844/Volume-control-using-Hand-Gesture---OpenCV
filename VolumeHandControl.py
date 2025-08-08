import cv2 
import time
import numpy as np
import hand_tracking_module as htm
import math
import os




############################################################################################################
wCam, hCam = 640, 480 #wCam = widthcam, hCam = heightcam
############################################################################################################

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
pTime = 0
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)

################################################################################################
#apple script for volume control
def set_volume(percent):
    os.system(f"osascript -e 'set volume output volume {percent}'")

min_vol = 0
max_vol = 100
#################################################################################################

vol_int = 0
vol_bar = 400
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
        # cv2.putText(img, f'{2}%',(x1,y1-20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        vol = np.interp(length, [20, 200], [min_vol, max_vol])
        vol_bar = np.interp(length, [20, 180], [400, 150])
        vol_int = int(vol)
        set_volume(vol_int)
        

        if length < 25:
            cv2.circle(img, (cx, cy), 7, (0,255,0), cv2.FILLED)
        elif length >= 200:
            cv2.circle(img, (cx, cy), 7, (0,0,255), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, f'Volume: {int(vol_int)}',(30, 130), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}',(40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

    cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

