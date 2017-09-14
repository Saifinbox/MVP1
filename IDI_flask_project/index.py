from flask import Flask
from flask import Flask, render_template, Response
import cStringIO as StringIO
from PIL import Image
import urllib2
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html') 

def gen(anom_type):
	try:
		host = "10.15.2.7:8080/video"
		hoststr = 'http://' + host

		stream=urllib2.urlopen(hoststr)

		bytes=''

		while True:
			bytes+=stream.read(1024)
			a = bytes.find('\xff\xd8')
			b = bytes.find('\xff\xd9')
			if a!=-1 and b!=-1:
				jpg = bytes[a:b+2]
				bytes= bytes[b+2:]
				streamline = StringIO.StringIO(jpg)
				img = Image.open(streamline)
				frame=np.array(img)
				yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')
	except Exception as e:
		pass

@app.route('/raspberry/<input_str>')
def raspberry(input_str):
	return Response(gen(input_str),
		mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run()
