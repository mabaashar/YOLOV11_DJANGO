from ultralytics import YOLO
import cv2
import math

from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings

class TonsillitisCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		self.model = YOLO('models/PPE.pt')
		#frame_width = int(self.video.get(3))
		#frame_height = int(self.video.get(4))
		self.classNames = self.model.names
		self.names = self.model.names

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		results = self.model(image,stream=True)
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

