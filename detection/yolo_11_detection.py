from ultralytics import YOLO
import cv2,os,urllib.request
import numpy as np
import math
from django.conf import settings


class yolo_11_detection(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		#load YOLO default nano model
		self.model = YOLO("static/detection/models/yolo11n.pt")

	def __del__(self):
		self.video.release()

	def get_frame_det(self):
		while True:
			ret, frame = self.video.read()
			if ret:
				#run YOLOV11 default nano model on the frame
				results = self.model(frame, conf=0.25, save=False)
				#loop over the results
				for result in results:
					boxes = result.boxes
					for box in boxes:
						x1, y1, x2, y2 = box.xyxy[0]
						#Convert the Tensor into integers
						x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
						print(f"x1:{x1}, y1: {y1}, x2:{x2}, y2:{y2}")
						cv2.rectangle(frame, (x1, y1), (x2, y2), [255,0,0], 2)
						#get the index of class name from the detected box
						classNameInt = int(box.cls[0])
						#get the class name
						classname = self.model.names[classNameInt]
						conf = math.ceil(box.conf[0] * 100)/100
						label  = classname + ":" + str(conf)
						text_size = cv2.getTextSize(label, 0, fontScale=0.5, thickness=2)[0]
						c2 = x1 + text_size[0], y1 - text_size[1] - 3
						#draw bonding box
						cv2.rectangle(frame, (x1, y1), c2, [255,0,0], -1)
						cv2.putText(frame, label, (x1, y1 - 2), 0, 0.5, [255,255,255], thickness=1, lineType=cv2.LINE_AA)
				
				ret, jpeg = cv2.imencode('.jpg', frame)
				#return frame
				return jpeg.tobytes()


