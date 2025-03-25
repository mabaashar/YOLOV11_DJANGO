#create threshold form
from django import forms
#from threshold.models import threshold_element
from threshold.models import threshold_component,yolo_model

class edit_threshold_element_form(forms.ModelForm):
    model1 = forms.ModelChoiceField(queryset=yolo_model.objects.all())
    model2 = forms.ModelChoiceField(queryset=yolo_model.objects.all())
    model3 = forms.ModelChoiceField(queryset=yolo_model.objects.all())
    model4 = forms.ModelChoiceField(queryset=yolo_model.objects.all())
    model5 = forms.ModelChoiceField(queryset=yolo_model.objects.all())

    class Meta:
        model = threshold_component
        fields = ('area1','cam_ip1','model1','cam1_active','area2','cam_ip2','model2','cam2_active','area3','cam_ip3','model3','cam3_active','area4','cam_ip4','model4','cam4_active','area5','cam_ip5','model5','cam5_active')
        exclude = ["user"],
    def __init__(self, *args, **kwargs):
        super(edit_threshold_element_form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

