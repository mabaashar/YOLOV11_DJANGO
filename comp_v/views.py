from django.shortcuts import render

def index(request):
    return render(request, 'dashboard.html', {})

def about(request):
    return render(request, 'about.html', {})