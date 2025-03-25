from ultralytics import YOLO
import cv2
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
		self.video = cv2.VideoCapture(self.db.cam_ip1)
		self.video.set(cv2.CAP_PROP_FRAME_COUNT, 10)
		self.video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
		# FPS = 1/X
		# X = desired FPS
		self.FPS = 1/30
		self.FPS_MS = int(self.FPS * 1000)

		#load model
		self.model = YOLO("static/threshold/models/yolo11n.pt")
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

	def get_frame(self): #update()
		while True:
			if self.video.isOpened():
				success, image = self.video.read()
				try:
					#resized_image = cv2.resize(image, (100, 50)) 
					print("first branch")
					#results = self.model(resized_image)
					results = self.model(image) 
					#results=image
				except Exception as e:
					print(e)
				return
				#Once we have the results we can check for individual bounding boxes and see how well it performs
				# Once we have have the results we will loop through them and we will have the bouning boxes for each of the result
				# we will loop through each of the bouning box
				for r in results:
					boxes=r.boxes
					for box in boxes:
						x1,y1,x2,y2=box.xyxy[0]
						x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
						print(x1,y1,x2,y2)
						#draw box
						cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,255),3)
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
						cv2.rectangle(image, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
						cv2.putText(image, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)

						#conclude frame with annotations
						ret, jpeg = cv2.imencode('.jpg', image)
				#return frame
				return jpeg.tobytes()
