from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from django.contrib import messages
#models
from ecommerce.accounts import EcomCustomer, EcomCustomerProfile
from threshold.models import Model_info,Image_upload,Video_upload,threshold_element

import time
import os
import time
#==================================================================

def profile(request):
        template = loader.get_template('ai/threshold.html')
        return HttpResponse(template.render({},request))

