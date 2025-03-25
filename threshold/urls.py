from django.urls import path
from . import views

app_name = 'threshold_app'
#first argument is how I want the path to look like
 
urlpatterns = [
    path('', views.threshold, name='threshold'),
    
    #dashboard
    path('t_dashboard/', views.t_dashboard, name='t_dashboard'),
    path('t_edit_profile/', views.t_edit_profile, name='t_edit_profile'),
    path('t_add_cam/', views.t_add_cam, name='t_add_cam'),

    path('model<int:chosen_model>/', views.threshold, name='threshold_by_model'),
    path('yolo_index/', views.cam_stream_index, name='cam_index'),
    path('yolo_v11_feed/', views.cam_stream, name='yolo_feed'),

]

