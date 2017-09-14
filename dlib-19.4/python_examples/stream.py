import urllib2
import numpy as np
import sys
from PIL import Image
import cStringIO as StringIO
from skimage import io

import dlib
import cv2

host = "10.15.2.7:8080/video"

hoststr = 'http://' + host
print 'Streaming ' + hoststr

stream=urllib2.urlopen(hoststr)

bytes=''
count=0
detector = dlib.simple_object_detector("detector.svm")
while True:
    count=count+1
    print(count)
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
	streamline = StringIO.StringIO(jpg)
	img = Image.open(streamline)
	print(img.size)
	img=np.array(img)
	dets = detector(img)
	for k, d in enumerate(dets):
		print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
		cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 255), 2)
		img = Image.fromarray(img)
		#img.save(str(count)+".jpg")
	#img.save(str(count)+".jpg")
	#io.imshow(img)
        #i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
	#image=np.fromstring(jpg, dtype=np.uint8)
	#print(len(image))
	#print(len(image))
        #cv2.imshow(hoststr,i)



	
