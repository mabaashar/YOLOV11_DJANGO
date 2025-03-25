from django.urls import path

from . import views

urlpatterns = [
    #yolo urls
    path("yolov11/", views.yolo_11, name="yolo_11"),
    #video feeds
    path("yolov11_detection/", views.yolo_11_det_feed, name="yolo_11_det"),
    path("yolov11_segmentation/", views.yolo_11_seg_feed, name="yolo_11_seg"),
    path("yolov11_pose/", views.yolo_11_pose_feed, name="yolo_11_pose"),


]