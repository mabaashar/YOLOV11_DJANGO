from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2,os,urllib.request
import numpy as np
import math
from django.conf import settings

class yolo_11_segment(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		#load YOLO default nano model
		self.model = YOLO("static/detection/models/yolo11n-seg.pt")

	def __del__(self):
		self.video.release()

	def get_frame_seg(self):
		while True:
			ret, im0 = self.video.read()
			print("in seg")
			if not ret:
				break

			results = self.model.predict(im0,show_labels=True, show_conf=True)
			im_copy = im0.copy()

			if results[0].masks is not None:
				#get class names
				clss = results[0].boxes.cls.cpu().tolist()
				masks = results[0].masks.xy
				#put class names on the frame
				for mask, cls in zip(masks, clss):
					color = colors(int(cls), True)
					#txt_color = annotator.get_txt_color(color)

				# Create binary mask
				b_mask = np.zeros(im0.shape[:2], np.uint8)

				# Extract contour and specify color (e.g. pink)
				contour = results[0].masks.xy[0].astype(np.int32).reshape(-1, 1, 2)
				#draw contour 
				im_copy = cv2.drawContours(im_copy, [contour], -1, (0, 0, 255), -1)
				alpha = 0.5
				filled = cv2.addWeighted(im0, alpha, im_copy, 1-alpha, 0)
				result = cv2.drawContours(filled, [contour], -1, (0, 0, 255), 0)

					
			ret, jpeg = cv2.imencode('.jpg', result)
			#return result
			return jpeg.tobytes()


