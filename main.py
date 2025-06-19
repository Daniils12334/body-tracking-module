import cv2
import mediapipe as mp
import time
from body_tracking_module.hand_tracking import HandsTracker
from body_tracking_module.pose_tracking import PoseTracker

pose_tracker = PoseTracker()
hand_tracker = HandsTracker()

cap = cv2.VideoCapture('/home/danbar/Desktop/body_tracking/videos/3.mp4')

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.resize(img, (1024, 600)) 
    img = pose_tracker.findPose(img, draw=True)
    poseLandmarks = pose_tracker.findPositions(img)

    img = hand_tracker.findHands(img)
    handLandmarksLeft = hand_tracker.findPosition(img, lmColor=(0,255,0), handNo=0, draw=True)
    handLandmarksRight = hand_tracker.findPosition(img, lmColor=(0,0,255), handNo=1, draw=True)

    if len(poseLandmarks) > 10:
        print("🧍‍♂️ Body landmark 10:", poseLandmarks[10])
    if len(handLandmarksLeft) > 10:
        print("👋 Left hand landmark 10:", handLandmarksLeft[10])
    if len(handLandmarksRight) > 10:
        print("✋ Right hand landmark 10:", handLandmarksRight[10])

    cv2.imshow("Image", img)
    cv2.waitKey(1)
