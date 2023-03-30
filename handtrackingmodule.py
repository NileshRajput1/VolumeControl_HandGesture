import time
import cv2
import mediapipe as mp

class HandDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, minDetectionConfidence=0.5, minTrackConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackConfidence = minTrackConfidence
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.minDetectionConfidence, self.minTrackConfidence)
        self.mpDraw = mp.solutions.drawing_utils

    def drawHands(self, img):
        """ To draw the detected hands on image """

        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        height,width,channels = img.shape
        lmList=[]
        if self.results.multi_hand_landmarks:
            handLms = self.results.multi_hand_landmarks[handNo]
            for id , lm in enumerate(handLms.landmark):
                x, y = int(lm.x*width), int(lm.y*height)
                lmList.append([id, x, y])
                if draw:
                    cv2.circle(img, (x,y), 10, (255,0,255), cv2.FILLED)

        return lmList


def main():
    pTime=0
    cTime=0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()

        img = detector.drawHands(img)
        lmList = detector.findPosition(img)
        if lmList:
            print(lmList[0])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,60), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)

        cv2.imshow("Image :",img)
        cv2.waitKey(1)

        if cv2.waitKey(32) == 32:
            break

    
if __name__ == "__main__":
    main()