import cv2
import mediapipe as mp
import time

class FaceTracker:
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)     

    def findFaces(self, img, draw = True):
        self.faceDetection

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []
        
        if self.results.detections:
            for id, detections in enumerate(self.results.detections):
                bboxC = detections.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                        int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detections.score])
                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detections.score[0]*100)}%', (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 2)
        return img, bboxs

    def fancyDraw(self, img, bbox, l = 20, t = 5, rt = 5):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(img, bbox, (255, 0, 255), rt)
        #Top Left x, y
        cv2.line(img, (x,y), (x+l, y), (255,0,255), t)
        cv2.line(img, (x,y), (x, y+l), (255,0,255), t)
        #Top Righr x1, y
        cv2.line(img, (x1,y), (x1-l, y), (255,0,255), t)
        cv2.line(img, (x1,y), (x1, y+l), (255,0,255), t)
        #Bottom Left x, y1
        cv2.line(img, (x,y1), (x+l, y1), (255,0,255), t)
        cv2.line(img, (x,y1), (x, y1-l), (255,0,255), t)
        #Bottom Right x1,y1
        cv2.line(img, (x1,y1), (x1-l, y1), (255,0,255), t)
        cv2.line(img, (x1,y1), (x1, y1-l), (255,0,255), t)

        return img


def main():
    cap = cv2.VideoCapture('videos/9.mp4')
    pTime = 0
    tracker = FaceTracker(0.4)
    while True:
        success, img = cap.read()
        if not success:
             break    

        img, bboxs = tracker.findFaces(img)
        if not success:
            break    
        print(bboxs)
        img = cv2.resize(img, (1024, 600))

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()