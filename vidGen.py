import cv2
import numpy as np
import pyqrcode
import png
import os
import shutil
import ffmpeg

os.mkdir('tempFrames')
os.mkdir('labeledFrames')

#Video Duration in Minutes:
duration = 3
#Framerate
fps = 60
totalFrames = duration * fps * 60

out = cv2.VideoWriter('qr_sync.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (290,290))


for i in range(0,totalFrames):
    data = i
    url = pyqrcode.create(data)
    url.png("tempFrames\\frame%d.png" % i, scale=10)
    
    image = cv2.imread("tempFrames\\frame%d.png" % i)
    coords = (115, 270)

    ms = i
    sec = ms/60
    min = sec/60

    timecode = "{:02d}:{:02d}:{:02d}".format(int(min%60), int(sec%60), int(ms%60))

    image = cv2.putText(image, timecode, coords, cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    cv2.imwrite("labeledFrames\\frame%d.png" % i, image)
    out.write(image)

out.release()

shutil.rmtree('tempFrames')
shutil.rmtree('labeledFrames')