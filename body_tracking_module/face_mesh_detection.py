import mediapipe as mp
import time
import cv2

class FaceMeshDetector():
    def __init__(self, staticMode=False, maxFaces = 2, minDetectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(
            static_image_mode=self.staticMode,
            max_num_faces=self.maxFaces,
            min_detection_confidence=self.minDetectionCon,
            min_tracking_confidence=self.minTrackCon
        )

        self.drawSpec = self.mpDraw.DrawingSpec(thickness=2, circle_radius=1, color=(0,255,0))

    def findFaceMesh(self, img, draw=True, drawId = False):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(imgRGB)
        faces = []
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        image=img,
                        landmark_list=faceLms,
                        connections=self.mpFaceMesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=self.drawSpec,
                        connection_drawing_spec=self.drawSpec
                    )
                face = []
                for id,lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    if drawId:
                        cv2.putText(img,str(id), (x+10,y), cv2.FONT_HERSHEY_PLAIN, 
                                    0.5, (0,255,0), 1)
                    face.append([x,y])
                faces.append(face)
        return img, faces

                    


def main():
    cap = cv2.VideoCapture("videos/11.mp4")
    pTime = 0
    detector = FaceMeshDetector()
    while True:
        success, img = cap.read()
        if not success:
            break
        img, faces = detector.findFaceMesh(img, draw=False, drawId=True)
        if len(faces) != 0:
            print(faces[0])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 
                    3, (0,255,0), 3)
        # img = cv2.resize(img, (1024, 600))
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()