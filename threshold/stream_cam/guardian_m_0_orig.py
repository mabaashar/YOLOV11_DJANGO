from ultralytics import YOLO
import math
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import threading
import queue
from ultralytics.utils.plotting import Annotator, colors
import time
#db
from threshold.models import threshold_component


class launch_module(object):
	def __init__(self,ob_req):
		#init db instance
		self.db = threshold_component.objects.get(user = ob_req.user)
		#init video capture
		#get available cam
		try:
			self.video1 = cv2.VideoCapture(self.db.cam_ip1,cv2.CAP_ANY)
		except Exception as e:
			self.video1 = None
			print(e)
		try:
			self.video2 = cv2.VideoCapture(self.db.cam_ip2,cv2.CAP_ANY)
		except Exception as e:
			self.video2 = None
			print(e)
		try:
			self.video3 = cv2.VideoCapture(self.db.cam_ip3,cv2.CAP_ANY)
		except Exception as e:
			self.video3 = None
			print(e)
		try:
			self.video4 = cv2.VideoCapture(self.db.cam_ip4,cv2.CAP_ANY)
		except Exception as e:
			self.video4 = None
			print(e)
		try:
			self.video5 = cv2.VideoCapture(self.db.cam_ip5,cv2.CAP_ANY)
		except Exception as e:
			self.video5 = None
			print(e)
		#self.video.set(cv2.CAP_PROP_FRAME_COUNT, 10)
		#1- set buffer size
		self.video1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
		# FPS = 1/X
		# X = desired FPS
		self.FPS = 1/2
		self.FPS_MS = int(self.FPS * 1000)
		#load models
		self.model1 = YOLO("static/threshold/models/yolo11n.pt")
		self.model2 = YOLO("static/threshold/models/yolo11n-seg.pt")
		self.model3 = YOLO("static/threshold/models/yolo11n-pose.pt")
		self.classNames = self.model1.names
		self.classNames2 = self.model2.names
		self.names = self.model1.names
		#run thread according to mode
		self.cam_ids = [5]
#------------------------------------------------------------------------------
		#for cam 1
		#for model 1
		print("in if active cams")
		print(self.db.model1.id)
		if self.db.cam1_active is True:
			print("cam 1 active")
			if self.db.model1.id== 1:
				self.cam_ids.append(1)
				self.thread = threading.Thread(target=self.get_frame, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 2
		if self.db.cam1_active is True:
			if self.db.model1.id == 2:
				self.cam_ids.append(2)
				self.thread = threading.Thread(target=self.get_seg, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 3
		if self.db.cam1_active is True:
			if self.db.model1.id == 3:
				self.cam_ids.append(3)
				self.thread = threading.Thread(target=self.get_pose, args=())
				self.thread.daemon = True
				self.thread.start()
#------------------------------------------------------------------------------
		#for cam 2
		#for model 1
		if self.db.cam2_active is True:
			if self.db.model2.id == 0:
				self.cam_ids.append(1)
				self.thread = threading.Thread(target=self.get_frame, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 2
		if self.db.cam2_active is True:
			if self.db.model2.id == 1:
				self.cam_ids.append(2)
				self.thread = threading.Thread(target=self.get_seg, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 3
		if self.db.cam2_active is True:
			if self.db.model2.id == 2:
				self.cam_ids.append(3)
				self.thread = threading.Thread(target=self.get_pose, args=())
				self.thread.daemon = True
				self.thread.start()
#------------------------------------------------------------------------------
		#for cam 3
		#for model 1
		if self.db.cam3_active is True:
			if self.db.model3.id == 0:
				self.cam_ids.append(1)
				self.thread = threading.Thread(target=self.get_frame, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 2
		if self.db.cam1_active is True:
			if self.db.model3.id == 1:
				self.cam_ids.append(2)
				self.thread = threading.Thread(target=self.get_seg, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 3
		if self.db.cam1_active is True:
			if self.db.model3.id == 2:
				self.cam_ids.append(3)
				self.thread = threading.Thread(target=self.get_pose, args=())
				self.thread.daemon = True
				self.thread.start()
#------------------------------------------------------------------------------
		#for cam 4
		#for model 1
		if self.db.cam4_active is True:
			if self.db.model4.id == 0:
				self.cam_ids.append(1)
				self.thread = threading.Thread(target=self.get_frame, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 2
		if self.db.cam4_active is True:
			if self.db.model4.id == 1:
				self.cam_ids.append(2)
				self.thread = threading.Thread(target=self.get_seg, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 3
		if self.db.cam4_active is True:
			if self.db.model4.id == 2:
				self.cam_ids.append(3)
				self.thread = threading.Thread(target=self.get_pose, args=())
				self.thread.daemon = True
				self.thread.start()
#------------------------------------------------------------------------------
		#for cam 5
		#for model 1
		if self.db.cam5_active is True:
			if self.db.model5.id == 0:
				self.cam_ids.append(1)
				self.thread = threading.Thread(target=self.get_frame, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 2
		if self.db.cam5_active is True:
			if self.db.model5.id == 1:
				self.cam_ids.append(2)
				self.thread = threading.Thread(target=self.get_seg, args=())
				self.thread.daemon = True
				self.thread.start()
		#for model 3
		if self.db.cam5_active is True:
			if self.db.model5.id == 2:
				self.cam_ids.append(3)
				self.thread = threading.Thread(target=self.get_pose, args=())
				self.thread.daemon = True
				self.thread.start()
#------------------------------------------------------------------------------


	def __del__(self):
		self.video1.release()

	def get_frame(self): #self.vido.read()
		while True:
			success, image = self.video1.read()
			#if image is None:
			#	return
			try:
				#resized_image = cv2.resize(image, (100, 50)) 
				#results = self.model(resized_image)
				resized=cv2.resize(image, (500,400), 0.5, 0.5,cv2.INTER_AREA);
				results = self.model1.predict(resized,show_labels=True, show_conf=True) 
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

	def get_seg(self): #self.vido.read()
		while True:
			print("get seg")
			success, image = self.video1.read()
			#if not success:
				#print("Video frame is empty or video processing has been successfully completed.")
				#continue
			results = self.model2.predict(image)
			annotator = Annotator(image, line_width=2)
			image_copy = image.copy()
			if results[0].masks is not None:
				#get class names
				clss = results[0].boxes.cls.cpu().tolist()
				masks = results[0].masks.xy
				#put class names on the frame
				for mask, cls in zip(masks, clss):
					color = colors(int(cls), True)
					txt_color = annotator.get_txt_color(color)
					annotator.seg_bbox(mask=mask, mask_color=color, label=self.classNames2[int(cls)], txt_color=txt_color)

				# Create binary mask
				b_mask = np.zeros(image.shape[:2], np.uint8)

				# Extract contour and specify color (e.g. pink)
				contour = results[0].masks.xy[0].astype(np.int32).reshape(-1, 1, 2)
				#draw contour 
				image_copy = cv2.drawContours(image, [contour], -1, (0, 0, 255), -1)
				alpha = 0.5
				filled = cv2.addWeighted(image, alpha, image_copy, 1-alpha, 0)
				result = cv2.drawContours(filled, [contour], -1, (0, 0, 255), 0)

				try:
					#conclude frame with annotations
					ret, jpeg = cv2.imencode('.jpg', result)
					#return frame
					return jpeg.tobytes()
				except Exception as e:
					print(e)
					continue

	def get_pose(self): #self.vido.read()
		while True:
			print("get pose")
			success, image = self.video1.read()
			if not success:
				continue
			# Run inference on the frame
			results = self.model3.predict(image,show_labels=True, show_conf=True) 
			# Plot results on frame
			annotated_frame = results[0].plot()
			try:
				#conclude frame with annotation
				ret, jpeg = cv2.imencode('.jpg', annotated_frame)
				#return frame
				return jpeg.tobytes()
			except Exception as e:
				print(e)
				continue

	def gen(camera):
		while True:
			frame = camera.get_frame()
			if frame is None:
				print("frame is none")
				return
			print("deddddd")
			#time.sleep(camera.FPS)
			yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	def gen_seg(camera):
		while True:
			frame = camera.get_seg()
			if frame is None:
				print("frame is none")
				return
			print("deddddd")
			#time.sleep(camera.FPS)
			yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	def gen_pose(camera):
		while True:
			frame = camera.get_pose()
			#if frame is None:
				#print("frame is none")
				#return
			print("deddddd")
			#time.sleep(camera.FPS)
			yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
