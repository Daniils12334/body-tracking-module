import cv2
import mediapipe
import time
import numpy as np

from body_tracking_module.pose_tracking import PoseTracker

ptm = PoseTracker()
count = 0
fdir = 0

pTime = 0

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    ptm.findPose(img, draw =False)
    lmList = ptm.findPositions(img)

    if len(lmList) != 0:
        angle = ptm.findAngle(img, 12, 14, 16)
        percent = np.interp(angle,(54, 150), (0,100))
        bar = np.interp(angle, (59, 150), (200, 480))

        if percent >= 90:
            if fdir == 0:
                count += 0.5
                fdir = 1
        if percent <= 10:
            if fdir == 1:
                count += 0.5
                fdir = 0

        cv2.rectangle(img, (0,200), (100, 480), (0, 255, 0), 3)
        cv2.rectangle(img, (0,int(bar)), (100, 480), (0, 255, 0), cv2.FILLED)

        cv2.putText(img, f'{count}', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10,30), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 1)

    cv2.imshow("Image", img)
    cv2.waitKey(1)