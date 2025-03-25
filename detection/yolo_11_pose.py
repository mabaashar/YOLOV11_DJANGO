from ultralytics import YOLO
import cv2,os,urllib.request
import numpy as np
import math
from django.conf import settings

class yolo_11_pose(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		#load YOLO default nano model
		self.model = YOLO("static/detection/models/yolo11n-pose.pt")

	def __del__(self):
		self.video.release()


	def get_frame_pose(self):
		while True:
			ret, frame = self.video.read()

			# Run inference on the frame
			results = self.model.predict(frame)

			# Plot results on frame
			annotated_frame = results[0].plot()
   
			ret, jpeg = cv2.imencode('.jpg', annotated_frame)
			#return annotated frame
			return jpeg.tobytes()


