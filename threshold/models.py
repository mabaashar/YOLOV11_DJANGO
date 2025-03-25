from django.db import models
from ecommerce.accounts import EcomCustomer
# Create your models here.
class Model_info(models.Model):
    name = models.CharField(max_length=200,null=False)
    describtion = models.CharField(max_length=900, null=True)
    image = models.ImageField(upload_to='static/threshold/models/img/')
class Image_upload(models.Model):
    user = models.ForeignKey(EcomCustomer, on_delete=models.CASCADE) 
    image = models.ImageField(blank=True,upload_to='static/threshold/img/')
class Video_upload(models.Model):
    user = models.ForeignKey(EcomCustomer, on_delete=models.CASCADE) 
    video = models.FileField(blank=True,upload_to='static/threshold/video/')

'''class threshold_element(models.Model):
    user = models.ForeignKey(EcomCustomer, on_delete=models.CASCADE)
    area1 = models.CharField(max_length=200,blank=True,default='x')
    cam_ip1 = models.CharField(max_length=900, blank=True,default='x')
    area2 = models.CharField(max_length=200,blank=True,default='x')
    cam_ip2 = models.CharField(max_length=900, blank=True,default='x')
    area3 = models.CharField(max_length=200,blank=True,default='x')
    cam_ip3 = models.CharField(max_length=900, blank=True,default='x')
    area4 = models.CharField(max_length=200,blank=True,default='x')
    cam_ip4 = models.CharField(max_length=900, blank=True,default='x')
    area5 = models.CharField(max_length=200,blank=True,default='x')
    cam_ip5 = models.CharField(max_length=900, blank=True,default='x')
'''

class yolo_model(models.Model):
    name = models.CharField(max_length=50)
    #fix plural
    class Meta:
        verbose_name_plural = "yolo_model"
    def __str__(self):
        return self.name
    @classmethod
    def get_default_pk(cls):
        yolo_model = cls.objects.get_or_create(
            title='default exam', 
            defaults=dict(description='this is not an exam'),
        )
        return yolo_model.pk

def get_yolo_model():
    return yolo_model.objects.get(id=1).name

class threshold_component(models.Model):
#    class Meta:
#        app_label = "t_comp"
#        managed = True
    user = models.ForeignKey(EcomCustomer, on_delete=models.CASCADE)
    area1 = models.CharField(max_length=200,blank=True)
    cam_ip1 = models.CharField(max_length=900, blank=True,)
    model1 = models.ForeignKey(yolo_model, related_name="ip_cam_1_model", on_delete=models.CASCADE,default=get_yolo_model())
    cam1_active = models.BooleanField(default=False)

    area2 = models.CharField(max_length=200,blank=True,)
    cam_ip2 = models.CharField(max_length=900, blank=True,)
    model2 = models.ForeignKey(yolo_model,related_name="ip_cam_2_model", on_delete=models.CASCADE,  default=get_yolo_model())
    cam2_active = models.BooleanField(default=False)

    area3 = models.CharField(max_length=200,blank=True,)
    cam_ip3 = models.CharField(max_length=900, blank=True,)
    model3 = models.ForeignKey(yolo_model,related_name="ip_cam_3_model", on_delete=models.CASCADE, default=get_yolo_model())
    cam3_active = models.BooleanField(default=False)

    area4 = models.CharField(max_length=200,blank=True,)
    cam_ip4 = models.CharField(max_length=900, blank=True,)
    model4 = models.ForeignKey(yolo_model,related_name="ip_cam_4_model", on_delete=models.CASCADE,  default=get_yolo_model())
    cam4_active = models.BooleanField(default=False)

    area5 = models.CharField(max_length=200,blank=True,)
    cam_ip5 = models.CharField(max_length=900, blank=True,)
    model5 = models.ForeignKey(yolo_model,related_name="ip_cam_5_model", on_delete=models.CASCADE,  default=get_yolo_model())
    cam5_active = models.BooleanField(default=False)
    #yolo_model = models.ForeignKey(Model_info,on_delete=models.CASCADE)
