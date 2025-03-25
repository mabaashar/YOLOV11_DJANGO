from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

#index view 
def index(request):
    return render(request, "dashboard.html", {})

#about view 
def about(request):
    return render(request, "about.html", {})