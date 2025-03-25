#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from django.contrib import messages

# from threshold.stream_cam import read_cam

from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import time
#threading
import threading
import queue

# models

from ecommerce.accounts import EcomCustomer, EcomCustomerProfile
from threshold.models import Model_info, Image_upload, Video_upload, \
    threshold_component

# forms

from threshold.forms import ImageUploadForm, VideoUploadForm,UploadVideoForm

# Imaginary function to handle an uploaded file.
#from website import handle_uploaded_file

# views

from threshold.dashboard import t_dashboard, t_edit_profile, t_add_cam

# YOLO PRED
# 1-YOLOV5 MODEL 1

from threshold.webapp.code.yolo_predictions import YOLO_Pred

# 2-YOLOV11 MODEL 2
# 3-live stream

from threshold.stream_cam.guardian_m_0 import launch_module
#from threshold.stream_cam.read_cam3 import launch_module

# ====================================================================
# LIBS

import PIL
from ultralytics import YOLO

# https://stackoverflow.com/questions/14348442/how-do-i-display-a-pil-image-object-in-a-template

from io import StringIO
from io import BytesIO
from PIL import Image
import cv2
import numpy
import numpy as np
import base64
import os
from pathlib import Path
import time
import math

# ==================================================================

def threshold(request, chosen_model=None):
    template = loader.get_template('ai/threshold.html')

    if chosen_model is None or chosen_model == '':
        return HttpResponse(template.render({'chosen_model': 0,
                            'chosen_flag': -1}, request))
#========================================================================================================
    elif chosen_model == 1:
        model_db = Model_info.objects.get(id=chosen_model)
        if request.POST:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():

                # get uploaded img

                uploaded = form.cleaned_data['image']

                # get its name

                c = request.FILES['image'].name

                # sleep here
                # messages.warning(request,"Uploading image...")

                time.sleep(3)

                # prepare YOLO PRED

                yolo = \
                    YOLO_Pred(onnx_model='threshold/webapp/models/model1.onnx'
                              ,
                              data_yaml='threshold/webapp/classes/model_1.yaml'
                              )
                myImage = uploaded.open('b+')
                with PIL.Image.open(myImage) as img_to_pred:
                    opencvImage = \
                        cv2.cvtColor(numpy.array(img_to_pred),
                            cv2.COLOR_BGRA2BGR)
                    img = yolo.predictions(opencvImage)

                # write to variable

                pil_img = Image.fromarray(img)
                img_to_pass = to_data_uri(pil_img)

                # original img
                # x =Image.fromarray()

                original = to_data_uri(img_to_pred)
                messages.success(request, 'Prediction made.')
                return HttpResponse(template.render({
                    'model_db': model_db,
                    'form': form,
                    'image': img_to_pass,
                    'original': original,
                    'results': img_to_pass,
                    'chosen_model': 1,
                    'chosen_flag': 0,
                    }, request))
        else:
            form = ImageUploadForm(request.POST, request.FILES)
            return HttpResponse(template.render({
                'model_db': model_db,
                'form': form,
                'chosen_model': 1,
                'chosen_flag': 0,
                }, request))
#========================================================================================================
    elif chosen_model == 2:
        model_db = Model_info.objects.get(id=chosen_model)
        if request.POST:
            form = ImageUploadForm(request.POST, request.FILES)

            # video_form = VideoUploadForm(request.POST,request.FILES)

            if form.is_valid():

                # get uploaded img

                uploaded = form.cleaned_data['image']

                # get uploaded video
                # uploaded_video = form.cleaned_data['video']
                # get image name

                try:
                    c = request.FILES['image'].name
                except Exception as e:
                    c = -1

                # get video name
                # try:
                    # v = request.FILES['video'].name
                # except Exception as e:
                    # v = -1
                # sleep here
                # messages.warning(request,"Uploading image...")

                time.sleep(3)

                # Load the YOLO11 Model

                model = YOLO('static/threshold/models/yolo11n.pt')

                # handle image

                if c != -1:
                    myImage = uploaded.open('b+')
                    with PIL.Image.open(myImage) as img_to_pred:
                        opencvImage = \
                            cv2.cvtColor(numpy.array(img_to_pred),
                                cv2.COLOR_BGRA2BGR)

                        # plot detections on image

                        img = model.predict(opencvImage)[0].plot()

                        # get the prediction text

                        pred_txt = model.predict(opencvImage)[0].names

                    # write to variable

                    pil_img = Image.fromarray(img)

                    # img = model.track(opencvImage)

                    img_to_pass = to_data_uri(pil_img)

                    # original img

                    x = Image.fromarray(opencvImage)
                    original = to_data_uri(x)
                    print(type(img_to_pass))
                    messages.success(request, 'Prediction made.')
                    return HttpResponse(template.render({
                        'model_db': model_db,
                        'form': form,
                        'image': img_to_pass,
                        'original': original,
                        'results': img,
                        'chosen_model': 2,
                        'chosen_flag': 0,
                        }, request))
        else:
            form = ImageUploadForm(request.POST, request.FILES)
            return HttpResponse(template.render({
                'model_db': model_db,
                'form': form,
                'chosen_model': 2,
                'chosen_flag': 0,
                }, request))
#========================================================================================================
    elif chosen_model == 3:
        model_db = Model_info.objects.get(id=chosen_model)
        if request.POST:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():

                # get uploaded img

                uploaded = form.cleaned_data['image']

                # get its name

                c = request.FILES['image'].name

                # sleep here
                # messages.warning(request,"Uploading image...")

                time.sleep(3)

                # Load the YOLO11 Model

                model = YOLO('static/threshold/models/yolo11n-seg.pt')

                myImage = uploaded.open('b+')
                with PIL.Image.open(myImage) as img_to_pred:
                    opencvImage = \
                        cv2.cvtColor(numpy.array(img_to_pred),
                            cv2.COLOR_BGRA2BGR)

                    # plot detections on image

                    img = model.predict(opencvImage)[0].plot()

                    # get the prediction text

                    pred_txt = model.predict(opencvImage)[0].names

                # write to variable

                pil_img = Image.fromarray(img)

                # img = model.track(opencvImage)

                img_to_pass = to_data_uri(pil_img)

                # original img

                x = Image.fromarray(opencvImage)
                original = to_data_uri(x)
                print(type(img_to_pass))
                messages.success(request, 'Prediction made.')
                return HttpResponse(template.render({
                    'model_db': model_db,
                    'form': form,
                    'image': img_to_pass,
                    'original': original,
                    'results': img,
                    'chosen_model': 3,
                    'chosen_flag': 0,
                    }, request))
        else:
            form = ImageUploadForm(request.POST, request.FILES)
            return HttpResponse(template.render({
                'model_db': model_db,
                'form': form,
                'chosen_model': 3,
                'chosen_flag': 0,
                }, request))
#========================================================================================================

    elif chosen_model == 4:
        model_db = Model_info.objects.get(id=chosen_model)
        if request.POST:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():

                # get uploaded img

                uploaded = form.cleaned_data['image']

                # get its name

                c = request.FILES['image'].name

                # sleep here
                # messages.warning(request,"Uploading image...")

                time.sleep(3)

                # Load the YOLO11 Model

                model = YOLO('static/threshold/models/yolo11n-pose.pt')

                myImage = uploaded.open('b+')
                with PIL.Image.open(myImage) as img_to_pred:
                    opencvImage = \
                        cv2.cvtColor(numpy.array(img_to_pred),
                            cv2.COLOR_BGRA2BGR)

                    # plot detections on image

                    img = model.predict(opencvImage)[0].plot()

                    # get the prediction text

                    pred_txt = model.predict(opencvImage)[0].names

                # write to variable

                pil_img = Image.fromarray(img)

                # img = model.track(opencvImage)

                img_to_pass = to_data_uri(pil_img)

                # original img

                x = Image.fromarray(opencvImage)
                original = to_data_uri(x)
                print(type(img_to_pass))
                messages.success(request, 'Prediction made.')
                return HttpResponse(template.render({
                    'model_db': model_db,
                    'form': form,
                    'image': img_to_pass,
                    'original': original,
                    'results': img,
                    'chosen_model': 4,
                    'chosen_flag': 0,
                    }, request))
        else:
            form = ImageUploadForm(request.POST, request.FILES)
            return HttpResponse(template.render({
                'model_db': model_db,
                'form': form,
                'chosen_model': 4,
                'chosen_flag': 0,
                }, request))
#========================================================================================================
    elif chosen_model == 5:
        model_db = Model_info.objects.get(id=chosen_model)
        if request.POST:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():

                # get uploaded img

                uploaded = form.cleaned_data['image']

                # get its name

                c = request.FILES['image'].name

                # sleep here
                # messages.warning(request,"Uploading image...")

                time.sleep(3)

                # Load the YOLO11 Model

                model = YOLO('static/threshold/models/ptholes_Y11.pt')

                myImage = uploaded.open('b+')
                with PIL.Image.open(myImage) as img_to_pred:
                    opencvImage = \
                        cv2.cvtColor(numpy.array(img_to_pred),
                            cv2.COLOR_BGRA2BGR)

                    # plot detections on image

                    img = model.predict(opencvImage)[0].plot()

                    # get the prediction text

                    pred_txt = model.predict(opencvImage)[0].names

                # write to variable

                pil_img = Image.fromarray(img)

                # img = model.track(opencvImage)

                img_to_pass = to_data_uri(pil_img)

                # original img

                x = Image.fromarray(opencvImage)
                original = to_data_uri(x)
                print(type(img_to_pass))
                messages.success(request, 'Prediction made.')
                return HttpResponse(template.render({
                    'model_db': model_db,
                    'form': form,
                    'image': img_to_pass,
                    'original': original,
                    'results': img,
                    'chosen_model': 5,
                    'chosen_flag': 0,
                    }, request))
        else:
            form = ImageUploadForm(request.POST, request.FILES)
            return HttpResponse(template.render({
                'model_db': model_db,
                'form': form,
                'chosen_model': 5,
                'chosen_flag': 0,
                }, request))
#========================================================================================================
    elif chosen_model == 6:
        model_db = Model_info.objects.get(id=chosen_model)
        if request.POST:
            form = UploadVideoForm(request.POST, request.FILES)

            # video_form = VideoUploadForm(request.POST,request.FILES)

            if form.is_valid():
                # get uploaded video
                print("handle upload")
                #uploaded = form.cleaned_data['video']
                uploaded = request.FILES["video"]
                print(type(uploaded))
                # get uploaded video
                # uploaded_video = form.cleaned_data['video']
                # get image name
                handle_uploaded_file(uploaded)
                print("handeled upesdf")
                try:
                    c = request.FILES['video'].name
                    p = uploaded.file.name
                    print(p)
                except Exception as e:
                    c = -1
                time.sleep(3)

                # Load the YOLO11 Model

                model = YOLO('static/threshold/models/yolo11n.pt')
                c = 23
                # handle image
                if c != -1:
                    #myVideo = uploaded.open('b+')
                    try:
                        cap=cv2.VideoCapture('uploadedVideo.avi')
                    except Exception as e:
                        print(e)
                    try:
                        out=cv2.VideoWriter('static/threshold/out.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (200, 200))
                    except Exception as e:
                        print(e)
                    while True:
                        success,img = cap.read()
                        # Doing detections using YOLOv8 frame by frame
                        #stream = True will use the generator and it is more efficient than normal
                        results=model(img,stream=True)
                        for r in results:
                            boxes=r.boxes
                            for box in boxes:
                                x1,y1,x2,y2=box.xyxy[0]
                                #print(x1, y1, x2, y2)
                                x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                                print(x1,y1,x2,y2)
                                cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
                                #print(box.conf[0])
                                conf=math.ceil((box.conf[0]*100))/100
                                #cls=int(box.cls[0])
                                class_name=model.names
                                label=f'{class_name}{conf}'
                                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                                #print(t_size)
                                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                                cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
                                cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
                        out.write(img)
                    return HttpResponse(template.render({
                        'model_db': model_db,
                        'form': form,
                        'video': cap,
                        'original': cap,
                        'results': out,
                        'chosen_model': 6,
                        'chosen_flag': 0,
                        }, request))
        else:
            form = UploadVideoForm()
            return HttpResponse(template.render({
                'model_db': model_db,
                'form': form,
                'chosen_model': 6,
                'chosen_flag': 0,
                }, request))
#========================================================================================================
    else:
        print('in last else')
        if chosen_model != 6:
            form = ImageUploadForm(request.POST, request.FILES)
            return HttpResponse(template.render({'form': form,
                                'chosen_model': chosen_model,
                                'chosen_flag': -1}, request))
        else:
            form = UploadVideoForm(request.POST, request.FILES)
            return HttpResponse(template.render({'form': form,
                                'chosen_model': chosen_model,
                                'chosen_flag': -1}, request))


# cam stream view

def cam_stream_index(request):

        # get DB instance

    tc = threshold_component.objects.get(user=request.user)
    return render(request, 'ai/cam_stream_11.html', {'user_data': tc})


# camera feed functions

@gzip.gzip_page
def cam_stream(request):
    print('in cam stream')
    #single thread
    cam = launch_module(request)
    print("alive")
    print(cam.p1.is_alive())
    print(type(cam))
    #return 0Streami0ngHttpResponse(gen(cam),content_type='multipart/x-mixed-replace; boundary=frame')
    #THreading
    #cam = launch_module(request)
    #thread = Thread(target = cam.get_frame, )
    #thread.start()
    #return StreamingHttpResponse(gen(thread),content_type='multipart/x-mixed-replace; boundary=frame')
    try:
        if cam.cam_ids[0] and cam.cam_ids[0] == 0 and cam.p1_alive == True:
            print("cam id is 0")
            return StreamingHttpResponse(cam.q1.get(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[0] and cam.cam_ids[0] == 1 and cam.p1_alive == True:
            print("cam id is 1")
            return StreamingHttpResponse(cam.q1.get(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[0] and cam.cam_ids[0] == 2 and cam.p1_alive == True:
            print("cam id is 2")
            return StreamingHttpResponse(cam.q1.get(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        '''
        elif cam.cam_ids[1] and cam.cam_ids[1] == 1:
            return StreamingHttpResponse(cam.gen(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[1] and cam.cam_ids[1] == 2:
            return StreamingHttpResponse(cam.gen_seg(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[1] and cam.cam_ids[1] == 3:
            return StreamingHttpResponse(cam.gen_pose(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[2] and cam.cam_ids[2] == 1:
            return StreamingHttpResponse(cam.gen(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[2] and cam.cam_ids[2] == 2:
            return StreamingHttpResponse(cam.gen_seg(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[2] and cam.cam_ids[2] == 3:
            return StreamingHttpResponse(cam.gen_pose(cam),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[3] and cam.cam_ids[3] == 1:
            return StreamingHttpResponse(cam.gen(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[3] and cam.cam_ids[3] == 2:
            return StreamingHttpResponse(cam.gen_seg(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[3] and cam.cam_ids[3] == 3:
            return StreamingHttpResponse(cam.gen_pose(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[4] and cam.cam_ids[4] == 1:
            return StreamingHttpResponse(cam.gen(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[4] and cam.cam_ids[4] == 2:
            return StreamingHttpResponse(cam.gen_seg(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
        elif cam.cam_ids[4] and cam.cam_ids[4] == 3:
            return StreamingHttpResponse(cam.gen_pose(),
                    content_type='multipart/x-mixed-replace;boundary=frame'
                    )
	'''
    except Exception as e:
        print('fffc now')
        print(e)
        print("xxxxx")

# Image conversion
def to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, 'JPEG')  # pick your format
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')

# Handeling uploads
def handle_uploaded_file(f):
    with open("uploadedVideo.avi", "wb+") as destination: #store it wherever you want
        for chunk in f.chunks():
            destination.write(chunk)
    print("handle_uploaded_file")
