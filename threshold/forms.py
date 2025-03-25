from django.db import models
from django import forms
from django.forms import ModelForm


from threshold.models import Image_upload, Video_upload

#model forms
class ImageUploadForm(ModelForm):
    image = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Image_upload 
        fields = ['image']

class VideoUploadForm(ModelForm):
    video = forms.FileField(required=False, error_messages = {'invalid':("Video files only")}, widget=forms.FileInput)
    class Meta:
        model = Video_upload
        fields = ['video']

#--------------------------------

#normal forms
class UploadVideoForm(forms.Form):
    video = forms.FileField()
