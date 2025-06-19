import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture('videos/11.mp4')
pTime = 0

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.90)

while True:
    success, img = cap.read()
    if not success:
        break
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        for id, detections in enumerate(results.detections):
            # mpDraw.draw_detection(img, detections)
            # print(id, detections)
            # print(detections.score)
            # print(detections.location_data.relative_bounding_box)
            bboxC = detections.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (255, 0, 255), 4)
            cv2.putText(img, f'{int(detections.score[0]*100)}%', (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 2)


    if img is None:
        break
    img = cv2.resize(img, (1024, 600))

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)