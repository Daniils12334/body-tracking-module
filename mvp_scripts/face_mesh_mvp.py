import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("videos/11.mp4")
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 2)
drawSpec = mpDraw.DrawingSpec(thickness=2, circle_radius=1, color=(0,255,0))

while True:
    success, img = cap.read()
    if not success:
        break
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(
                image=img,
                landmark_list=faceLms,
                connections=mpFaceMesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawSpec,
                connection_drawing_spec=drawSpec
            )
            for id,lm in enumerate(faceLms.landmark):
                ih, iw, ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                print(id, x, y)
                
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 
                3, (0,255,0), 3)
    img = cv2.resize(img, (1024, 600))
    cv2.imshow("Image", img)
    cv2.waitKey(1)