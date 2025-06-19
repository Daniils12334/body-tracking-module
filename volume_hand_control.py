from body_tracking_module.hand_tracking import HandsTracker

import cv2
import time
import numpy as np
import math

import pulsectl

pulse = pulsectl.Pulse('volume-controller')
sinks = pulse.sink_list()
sink = sinks[0]
volume = float(sink.volume.value_flat)


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4,hCam)
pTime = 0

detector = HandsTracker()

while True:
    success, img = cap.read()
    if not success:
        break

    detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) > 0:

        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (0,255,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0,255,0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 3)
        cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        print(int(length))

        minLength = 50
        maxLength = 300
        normalized = max(0, min(1, (length - minLength) / (maxLength - minLength)))

        color = (int(255 * normalized), int(255 * (1 - normalized)), 0)
        cv2.circle(img, (cx, cy), 15, color, cv2.FILLED)

        pulse.volume_set_all_chans(sink, normalized)

        value = int(normalized * 100)
        text_color = (0, 255 - int(2.55 * value), int(2.55 * value))

        cv2.putText(img, f'Volume: {value}%', (20, 80),
                    cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 2)

        if value < 20:
            label = "White noise enjoyer"
        elif value < 60:
            label = "Classic Music Enjoyer"
        elif value < 90:
            label = "Rock Enjoyer"
        else:
            label = "Death Metal Enjoyer"

        cv2.putText(img, label, (20, 120), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 2)

        bar_x, bar_y = 50, 440
        bar_width, bar_height = 540, 20
        fill_width = int(bar_width * normalized)

        cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 2)
        cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), text_color, cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)



    cv2.imshow("Img", img)
    cv2.waitKey(1)
