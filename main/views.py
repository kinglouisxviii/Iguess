from django.shortcuts import render_to_response, render
from django import forms
from main.RegisterForm import *
from main.LoginForm import *
from django.http import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from main.models import Player
# Create your views here.
def register(request):
	error = {'username': '', 'email': '', 'password2': ''}
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		error = form.errors
		if form.is_valid():
			confirm = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password2'])
			confirm.save
			foreign = Player(username = form.cleaned_data['username'], email = form.cleaned_data['email'], totalgame = 0, totalwin = 0, times_today = 0, percent = 0)
			foreign.save()
			return HttpResponseRedirect('/login/')
	else:
		form = RegisterForm()
	return render_to_response('register.html',{'error_user': error['username'], 'error_email': error['email'], 'error_password': error['password2']})

def login_view(request):
	error = False
	if request.user.is_authenticated():
		return HttpResponse('already authenticate')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/index/')
			else:
				error = True
				return render_to_response('login.html', {'error': error, 'errorvalue': 'account disabled'})
		else:
			error = True
			return render_to_response('login.html', {'error': error, 'errorvalue': 'Username or Password is wrong'})
	else:
		pass
	return render_to_response('login.html')

def logout_view(request):
	logout(request)
	return render_to_response('index.html')

def index(request):
	return render(request, 'index.html')