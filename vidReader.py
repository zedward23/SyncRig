import cv2
import numpy as np
import pyqrcode
import png
import os
import shutil
import ffmpeg

reader = cv2.QRCodeDetector()

captures = []

dir = "testData"

firstFrames = []

for filename in os.listdir(dir):    
    cap = cv2.VideoCapture(dir + "\\" + filename)
    qrDetected = False
    frameNo = 0
    while not qrDetected:
        isFrame, frame = cap.read()
        data, bbox, _ = reader.detectAndDecode(frame)
        if (frameNo % 50 == 0):
            print("Processing Frame ", frameNo, " of ", filename)
        if data:
            print("Code detected in frame ", str(frameNo), " of ", filename, " data:", data)
            qrDetected = True
            firstFrames.append((data, frame))
            cv2.imwrite("frame%d.png" % frameNo, frame)
        if not isFrame:
            print("No Frame Detected in ", filename)
            break
        frameNo += 1

#cv2.imshow(firstFrames[0][0], firstFrames[0][1])
#cv2.waitKey(100)
#cv2.imshow(firstFrames[1][0], firstFrames[1][1])
#cv2.waitKey(100)

