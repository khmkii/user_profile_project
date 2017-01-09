from django.shortcuts import render

from accounts import models


def home(request):
    users = models.UserProfile.objects.all()
    return render(request, 'home.html', {'users': users})
