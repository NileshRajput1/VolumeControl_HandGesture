import cv2
import time
import handtrackingmodule as htm
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam, hCam = 640,480 #width and height of camera

# initializations for getting and setting volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


volRange = volume.GetVolumeRange()


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
volumeBar = 400

detector = htm.HandDetector()


while True:
    success, img = cap.read()
    detector.drawHands(img)

    
    

    lmList = detector.findPosition(img, draw=False)

    if lmList:
        thumb, indexFinger = lmList[4], lmList[8]
        # print(thumb, indexFinger)
        x1, y1 = thumb[1], thumb[2]
        x2, y2 = indexFinger[1], indexFinger[2]
        

        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0,0,0))

        length = math.dist((x1,y1), (x2, y2))
        print(length)


        # Hand Length range = 30 to 180
        # Volume range = -65.25 to 0
        handRange = [30, 180]
        
        volumeBar = np.interp(length, [30,180], [400,150])

        if length<handRange[0]:
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            cv2.circle(img, (cx, cy), 15, (0,0,255), cv2.FILLED)
            volume.SetMasterVolumeLevel(-65.25, None)

        elif length<handRange[1]:
            vol = np.interp(length, handRange, volRange[:2])
            volume.SetMasterVolumeLevel(vol, None)
        
        else:
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            cv2.circle(img, (cx, cy), 15, (0,255,0), cv2.FILLED)
            volume.SetMasterVolumeLevel(0, None)

    
    cv2.rectangle(img, (50,150), (85, 400), (0,255,0), 3)
    cv2.rectangle(img, (50, int(volumeBar)), (85,400), (0,255,0), cv2.FILLED)  

    # getting frames per second of video
    cTime = time.time() #current time
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,60), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,255), 5)

    cv2.imshow("Image :",img)
    cv2.waitKey(1)

    if cv2.waitKey(32) == 32:
        break