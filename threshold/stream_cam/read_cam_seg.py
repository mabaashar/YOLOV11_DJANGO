'''from ultralytics import YOLO
import math
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import threading
import time
#db
from threshold.models import threshold_component


class launch_module(object):
	def __init__(self,ob_req):
		#init db instance
		self.db = threshold_component.objects.get(user = ob_req.user)
		#init video capture
		#self.video = cv2.VideoCapture('rtsp://admin:Gotellauntrhody000@0.tcp.in.ngrok.io:12995')
		#get available cams
		self.video = cv2.VideoCapture(self.db.cam_ip1,cv2.CAP_ANY)

		#self.video.set(cv2.CAP_PROP_FRAME_COUNT, 10)
		#1- set buffer size
		self.video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
		# FPS = 1/X
		# X = desired FPS
		self.FPS = 1/2
		self.FPS_MS = int(self.FPS * 1000)
                #load models
		self.model = YOLO("static/threshold/models/yolo11n.pt")
		self.model2 = YOLO("static/threshold/models/yolo11n-seg.pt")
		self.model3 = YOLO("static/threshold/models/yolo11n-pose.pt")

		#frame_width = int(self.video.get(3))
		#frame_height = int(self.video.get(4))
		self.classNames = self.model.names
		self.names = self.model.names
		#threading
		# Start frame retrieval thread
		self.thread = threading.Thread(target=self.get_frame, args=())
		self.thread.daemon = True
		self.thread.start()

	def __del__(self):
		self.video.release()

	def get_frame(self): #self.vido.read()
		while True:
			success, image = self.video.read()
			#if image is None:
			#	return
			try:
				#resized_image = cv2.resize(image, (100, 50)) 
				#results = self.model(resized_image)
				resized=cv2.resize(image, (500,400), 0.5, 0.5,cv2.INTER_AREA);
				results = self.model2(resized) 
				#results=image
			except Exception as e:
				print(e)
				return
			print("sleep now")
			time.sleep(self.FPS)
			for r in results:
				boxes=r.boxes
				for box in boxes:
					x1,y1,x2,y2=box.xyxy[0]
					x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
					print(x1,y1,x2,y2)
					#draw box
					cv2.rectangle(resized, (x1,y1), (x2,y2), (255,0,255),3)
					#print(box.conf[0])
					#get confidence
					conf=math.ceil((box.conf[0]*100))/100
					#get class id
					cls=int(box.cls[0])
					class_name=self.classNames[cls]
					#detect human now
					if class_name == 'person' and conf > 0.5:
						print("person for sure !!")
					#visualize label
					label=f'{class_name}{conf}'
					t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
					c2 = x1 + t_size[0], y1 - t_size[1] - 3
					#draw label
					cv2.rectangle(resized, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
					cv2.putText(resized, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
			try:
				#conclude frame with annotations
				ret, jpeg = cv2.imencode('.jpg', resized)
				#return frame
				return jpeg.tobytes()
			except Exception as e:
				print(e)
				continue


def update(self):
		while True:
			(self.grabbed, self.frame) = self.video.read()


def gen(camera):
		while True:
			frame = camera.get_frame()
			yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def livefe(request):
		try:
			cam = VideoCamera()
			return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
		except:  # This is bad! replace it with proper handling
			pass

'''

