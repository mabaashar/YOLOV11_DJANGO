#===========================================
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.db import connection
from django.core.management.color import no_style
import json

#models
from ecommerce.accounts import EcomCustomer, EcomCustomerProfile
from threshold.models import Model_info,Image_upload,Video_upload,threshold_component

#forms
from threshold.edit_threshold_form import edit_threshold_element_form
from threshold.add_threshold_form import add_cam_form
#from threshold.add_threshold_form import add_threshold_element_form

#pagination
#from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Threshold profile
@login_required(login_url='user_login')
def t_dashboard(request):
    userprofile = EcomCustomerProfile.objects.get(user_id=request.user.id)
    #get user's threshold element(s)
    t_elements = threshold_component.objects.filter(user_id=request.user.id)
    #user_cams = t_elements.count()
    #get number of cams
    user_cams = 0
    for x in t_elements:
        if x.cam_ip1 != '':
            user_cams = user_cams +1
        if x.cam_ip2 != '':
            user_cams = user_cams +1
        if x.cam_ip3 != '':
            user_cams = user_cams +1
        if x.cam_ip4 != '':
            user_cams = user_cams +1
        if x.cam_ip5 != '':
            user_cams = user_cams +1

    messages.success(request, 'The threshold welcomes you')
    context = {
        'user':request.user,
        'profile':userprofile,
        'number_cams':user_cams,

    }
    return render(request, 'ai/dashboard.html',context)

@login_required
def t_edit_profile(request):
    user = request.user
    try:
        past_values = threshold_component.objects.get(user = user)
        print("got past values")
    except Exception as e:
        past_values = None
        print(e)
        messages.error(request, 'You didn''t enter a camera before. Add one please')
        return redirect('threshold_app:t_add_cam')

    if request.method == 'POST':
        form = edit_threshold_element_form(request.POST,instance=past_values)
        if form.is_valid():
            #insert values 
            # get the data of the user
            user_data = threshold_component.objects.get(user_id = user.id)
            # get the form data
            area1 = form.cleaned_data['area1']
            cam_ip1 = form.cleaned_data['cam_ip1']
            model1 = form.cleaned_data['model1']

            area2 = form.cleaned_data['area2']
            cam_ip2 = form.cleaned_data['cam_ip2']
            model2 = form.cleaned_data['model2']

            area3 = form.cleaned_data['area3']
            cam_ip3 = form.cleaned_data['cam_ip3']
            model3 = form.cleaned_data['model3']

            area4 = form.cleaned_data['area4']
            cam_ip4 = form.cleaned_data['cam_ip4']
            model4 = form.cleaned_data['model4']

            area5 = form.cleaned_data['area5']
            cam_ip5 = form.cleaned_data['cam_ip5']
            model5 = form.cleaned_data['model5']

            #insert in db according to field and skip blank
            if area1 != '':
                 user_data.area1 = area1
            if cam_ip1 is not '':
                 user_data.cam_ip1 = cam_ip1
            if model1 is not '':
                 user_data.model1 =  model1

            if area2 != '':
                 user_data.area2 = area2
            if cam_ip2 != '':
                 user_data.cam_ip2 = cam_ip2
            if model2 is not '':
                 user_data.model2 =  model2

            if area3 != '':
                 user_data.area3 = area3
            if cam_ip2 != '':
                 user_data.cam_ip3 = cam_ip3
            if model3 is not '':
                 user_data.model3 =  model3

            if area4 is not '':
                 user_data.area4 = area4
            if cam_ip4 != '':
                 user_data.cam_ip4 = cam_ip4
            if model4 is not '':
                 user_data.model4 =  model4

            if area5 != '':
                 user_data.area5 = area5
            if cam_ip5 != '':
                 user_data.cam_ip5 = cam_ip5
            if model5 is not '':
                 user_data.model5 =  model5

            #needed error fix
            form.instance.user = EcomCustomer.objects.get(email=request.user)
            form.save()
            messages.success(request, 'Your cam(s) have been updated.')
            return redirect('threshold_app:t_dashboard')
    else:
        if past_values:
            form = edit_threshold_element_form(instance=past_values)
        else:
            form = edit_threshold_element_form(instance=past_values,initial={'model1': '1','model2': '1','model3': '1','model4': '1','model5':'1'})

    context = {'form': form,}
    return render(request, 'ai/edit_profile.html', context)

@login_required
def t_add_cam(request):
    user = request.user
    try:
        past_values = threshold_component.objects.get(user = user)
        print("got past values")
    except Exception as e:
        past_values = None
        print(e)
        reset_sequence(threshold_component)
        pass
    #reset_sequence(threshold_component)
    user = request.user
    print("45r45")
    if request.method == 'POST':
        print("post")
        form = add_cam_form(request.POST,instance=past_values)
        if form.is_valid():
            #insert values 
            # get the data
            # get the form data
            area1 = form.cleaned_data['area1']
            cam_ip1 = form.cleaned_data['cam_ip1']
            model1 = form.cleaned_data['model1']

            area2 = form.cleaned_data['area2']
            cam_ip2 = form.cleaned_data['cam_ip2']
            model2 = form.cleaned_data['model2']

            area3 = form.cleaned_data['area3']
            cam_ip3 = form.cleaned_data['cam_ip3']
            model3 = form.cleaned_data['model3']

            area4 = form.cleaned_data['area4']
            cam_ip4 = form.cleaned_data['cam_ip4']
            model4 = form.cleaned_data['model4']

            area5 = form.cleaned_data['area5']
            cam_ip5 = form.cleaned_data['cam_ip5']
            model5 = form.cleaned_data['model5']


            #insert in db according to field and skip blank
            if area1 != '':
                 form.area1 = area1
            if cam_ip1 is not '':
                 form.cam_ip1 = cam_ip1
            if model1 is not '':
                 form.model1 =  model1
            else:
                 form.model1 =  1

            if area2 != '':
                 form.area2 = area2
            if cam_ip2 != '':
                 form.cam_ip2 = cam_ip2
            if model2 is not '':
                 form.model2 =  model2
            else:
                 form.model2 =  1

            if area3 != '':
                 form.area3 = area3
            if cam_ip2 != '':
                 form.cam_ip3 = cam_ip3
            if model3 is not '':
                 form.model3 =  model3
            else:
                 form.model3 =  1

            if area4 is not '':
                 form.area4 = area4
            if cam_ip4 != '':
                 form.cam_ip4 = cam_ip4
            if model4 is not '':
                 form.model4 =  model4
            else:
                 form.model4 =  1

            if area5 != '':
                 form.area5 = area5
            if cam_ip5 != '':
                 form.cam_ip5 = cam_ip5
            if model5 is not '':
                 form.model5 =  model5
            else:
                 form.model5 =  1
            #needed error fix
            form.instance.user = EcomCustomer.objects.get(email=request.user)
            print(form.errors)
            form.save()
            messages.success(request, 'Your cam(s) have been updated.')
            return redirect('threshold_app:t_dashboard')
    else:
        if past_values:
            form = add_cam_form(instance=past_values)
        else:
            form = add_cam_form(instance=past_values,initial={'model1': '1','model2': '1','model3': '1','model4': '1','model5': '1',})
        print("else")
    context = {'form': form,}
    return render(request, 'ai/add_cam.html', context)

def reset_sequence(instance_reset):
    #reset sequence
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [instance_reset])
    with connection.cursor() as cursor:
         for sql in sequence_sql:
             cursor.execute(sql)
    print("sequence reset")

