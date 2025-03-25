from django.shortcuts import render, reverse
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from detection.yolo_11_detection import yolo_11_detection as get_detection_frame
from detection.yolo_11_segment import yolo_11_segment as get_segmentation_frame
from detection.yolo_11_pose import yolo_11_pose as get_pose_frame

#yolov11 view 
def yolo_11(request):
    #get the yolo model choice from template
    yolom = request.GET.get('yolom')
    print(yolom)
    return render(request, "cam_stream.html", {'yolo_model':yolom})

#generate video as an image view
def gen(camera):
    while True:
        print("in gen")
        frame = camera.get_frame_det()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen_segment(camera):
    while True:
        print("in gen_segment")
        frame = camera.get_frame_seg()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen_pose(camera):
    while True:
        print("in gen_pose")
        frame = camera.get_frame_pose()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#return StreamingHttpResponse generating an instance of "yolo_11_detection"
def yolo_11_det_feed(request):
    return StreamingHttpResponse(gen(get_detection_frame()),
                    content_type='multipart/x-mixed-replace; boundary=frame')

#return StreamingHttpResponse generating an instance of "yolo_11_segment"
def yolo_11_seg_feed(request):
    return StreamingHttpResponse(gen_segment(get_segmentation_frame()),
                    content_type='multipart/x-mixed-replace; boundary=frame')

#return StreamingHttpResponse generating an instance of "yolo_11_pose"
def yolo_11_pose_feed(request):
    return StreamingHttpResponse(gen_pose(get_pose_frame()),
                    content_type='multipart/x-mixed-replace; boundary=frame')