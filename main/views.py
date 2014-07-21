from django.shortcuts import render_to_response, render
from django import forms
from main.RegisterForm import *
from main.LoginForm import *
from django.http import *
from django.core.exceptions import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from main.models import Player
from main.models import Topic
from datetime import *
from main.models import Player_Topic
# Create your views here.
def register(request):
	error = {'username': '', 'email': '', 'password2': ''}
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		error = form.errors
		if form.is_valid():
			confirm = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password2'])
			confirm.save
			u = User.objects.get(username = form.cleaned_data['username'])	
			foreign = Player(username = u, email = form.cleaned_data['email'], totalgame = 0, totalwin = 0, times_today = 0, percent = 0, money = 100, user_id = u.id, last_reg = date.today())
			foreign.save()
			return HttpResponseRedirect('/login/')
	else:
		form = RegisterForm()
	return render_to_response('register.html', {'error_user': error.get('username'), 'error_email': error.get('email'), 'error_password': error.get('password2')})

def login_view(request):
	error = False
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				p = Player.objects.get(username = username)
				if p.last_reg < date.today():
					p.money += 10
					p.last_reg = date.today()
					p.save()
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

class searchForm(forms.Form):
	title = forms.CharField(max_length = 16, required=False)

def index(request):
	form = searchForm(request.GET)
	topics = Topic.objects.filter(due__gte = datetime.now()).order_by('?')
	if 'title' in request.GET:
		title = request.GET['title']
		topics = topics.filter(title__icontains=title)
	# exclude topics already answered
	for tpc in topics:
		if Player_Topic.objects.filter(topic_id = tpc.id, user_id = request.user.id).exists():
			topics = topics.exclude(id = tpc.id)
	topics = topics[:6]
	return render(request, 'index.html', {'topics': topics, 'form': form})

def choose(request):
	if request.method == 'POST':
		if request.user.is_authenticated():
			user_ID = request.user.id
			topic_ID = request.POST['id']
			if Player_Topic.objects.filter(user_id = user_ID, topic_id = topic_ID).exists():
				return HttpResponse('You have already bet this topic')
			if Topic.objects.get(id = topic_ID).due.replace(tzinfo=None) < datetime.now():
				return HttpResponse('This topic is already due')
			p = Player.objects.get(user_id = user_ID)
			p.totalgame += 1
			p.save()
			choice = bool(int(request.POST['choice']))
			new = Player_Topic()
			new.user_id = user_ID
			new.topic_id = topic_ID
			new.choice = choice
			new.save()
			return HttpResponseRedirect('/index/')
		return HttpResponseRedirect('/login/', {'request': request})

def rank(request):
	if request.user.is_authenticated():
		rank = Player.objects.order_by('money')
		rank = rank[:10]
		return render(request,'rank.html',{'rank': rank})
	return render(request,'rank.html')


def myaccount(request):
	if request.user.is_authenticated():
		userid = request.user.id
		p = Player.objects.get(user_id = userid)
		return render(request,'account.html',{'p': p})
	else:
		return HttpResponseRedirect('/index',{'request', request})