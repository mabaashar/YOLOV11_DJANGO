from django.contrib import admin

from threshold.models import Image_upload,Model_info,Video_upload,threshold_component,yolo_model
# Register your models here.

admin.site.register(Image_upload)
admin.site.register(Model_info)
admin.site.register(threshold_component)
admin.site.register(yolo_model)
