import skvideo.io

import numpy as np 


import os
import sys
import glob

import dlib
from skimage import io
import cv2



# read video as a single ndarray
# read video frame by frame
videogen = skvideo.io.vreader("ciggtestvideo.mp4")
writer = skvideo.io.FFmpegWriter("ciggoutputvideo.mp4")
detector = dlib.simple_object_detector("cigg_detector.svm")
for frame in videogen:
    print(type(frame))    
    dets = detector(frame)
    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
	cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 255), 2)
	writer.writeFrame(frame)
writer.close()
