from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# from login.models import Users
# Create your views here.
# from home.models import Users

def login(request):
	if request.user.is_authenticated:
		return redirect('home:index')
	else:
		return redirect('login')

 