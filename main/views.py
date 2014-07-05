from django.shortcuts import render_to_response
from django import forms
from main.RegisterForm import *
from django.http import *
from django.template import RequestContext
from main.models import User
import hashlib
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def register(request):
	error = {}
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		error = form.errors
		if form.is_valid():
			confirm = User(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = hashlib.sha1(form.cleaned_data['password2']).hexdigest(), totalwin = 0, totalgame = 0, percent = 0.0, times_today = 0)
			confirm.save()
			return HttpResponseRedirect('/login/')
	else:
		form = RegisterForm()
	return render_to_response('register.html',{'error': error})

class login_form(forms.Form):
	username = forms.CharField(max_length = 16)
	password = forms.CharField(max_length = 40, widget = forms.PasswordInput)


def login_view(request):
	username = ''
	password = ''
	if request.method == 'POST':	
		form = login_form(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = hashlib.sha1(form.cleaned_data['password']).hexdigest()
			user = User.objects.filter(username = username, password = password)
			if user:
				return HttpResponseRedirect('/index/')
	else:
		form = login_form()
	return render_to_response('login.html')

def index(request):
	return render_to_response('index.html')