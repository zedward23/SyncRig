import cv2
import numpy as np
import pyqrcode
import png
import os
import shutil
import ffmpeg
from moviepy.editor import VideoFileClip, concatenate_videoclips

def pad_to_sync(firstFrames, fps):
    
    # take id <-> first frame number 
    anchorTake = 0

    #firstFrames is n x 4
    earliestFrame = firstFrames[anchorTake] # 1 x 4

    for i in range(0,len(firstFrames)):
        if firstFrames[i][1] < earliestFrame[1]:
            anchorTake = i
            earliestFrame = firstFrames[anchorTake]

    anchor = firstFrames.pop(anchorTake) # 1 x 4
    
    #trim anchor
    clip = VideoFileClip(anchor[2])
    clip = clip.subclip(anchor[0]/fps, clip.duration)
    clip.write_videofile("merged_"+anchor[2], codec='libx264', fps=fps)

    for elt in firstFrames:
        genPad(elt, fps, anchor)
        join(fps, elt[2], elt[0])
    

    return

def genPad(currTake, fps, anchor):
    # take id <-> first frame number 
    
    out = cv2.VideoWriter('padding.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (anchor[3].shape[1], anchor[3].shape[0]))
    blank = cv2.imread("blank.png")

    qr_delta = currTake[1] - anchor[1]
    
    print(qr_delta)
    for i in range(0,qr_delta):
        out.write(blank)
    
    out.release()
    print("Padding Complete")

def join(fps, filename, currFrame):

    clip1 = VideoFileClip("padding.mp4")
    clip2 = VideoFileClip(filename)

    final_clip = concatenate_videoclips([clip1,clip2.subclip(currFrame/fps,clip2.duration)])
    final_clip.write_videofile("merged_"+filename, codec='libx264', fps=fps)



frame1 = cv2.imread("frame2057.png")
frame2 = cv2.imread("frame1528.png")

print(frame1.shape)
#firstFrames; frameNum, QRtimeCode, filename, frameData

#Frame Diff 529
#QR Diff 375

firstFrames = [(2057, 628, "testData\\GX010221.MP4", frame1), 
               (1528, 253, "testData\\GX010261.MP4", frame2)]

pad_to_sync(firstFrames, 60)