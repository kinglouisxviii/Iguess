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
from django.contrib.admin.views.decorators import staff_member_required
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
				try:
					p = Player.objects.get(username = username)
				except Player.DoesNotExist:
					pass
				else:
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
	topics = Topic.objects.filter(due__gte=datetime.now(), active=True).order_by('?')
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
			bet = request.POST['bet']
			try:
				bet = int(bet)
			except:
				return HttpResponse('please enter an integer bet')
			if Player_Topic.objects.filter(user_id = user_ID, topic_id = topic_ID).exists():
				return HttpResponse('You have already bet this topic')
			if Topic.objects.get(id = topic_ID).due.replace(tzinfo=None) < datetime.now():
				return HttpResponse('This topic is already due')
			try:
				p = Player.objects.get(user_id = user_ID)
				if(p.money < bet):
					return HttpResponse('You don\'t have enough money for this bet\nYou have only '+ str(p.money) +' left')
				p.totalgame += 1
				p.money -= bet
				p.save()
				choice = bool(int(request.POST['choice']))
				new = Player_Topic()
				new.user_id = user_ID
				new.topic_id = topic_ID
				new.choice = choice
				new.bet = bet
				new.save()
			except Player.DoesNotExist:
				pass
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
		try:
			p = Player.objects.get(user_id = userid)
		except Player.DoesNotExist:
			return HttpResponse('I\' m the superuser')
		return render(request,'account.html',{'p': p})
	else:
		return HttpResponseRedirect('/index',{'request', request})

def myguess(request):
	if request.user.is_authenticated():
		userid = request.user.id
		tp = Player_Topic.objects.filter(user_id = userid)
		topics = []
		for i in tp:
			item = Topic.objects.get(id = i.topic_id)
			topics = topics.add(item)
		return render(request,'index.html',{'topics': topics})
	else:
		return HttpResponseRedirect('/index',{'request', request})

@staff_member_required
def edit(request):
	if request.method == 'POST':
		topic_ID = request.POST['id']
		choice = bool(int(request.POST['choice']))
		topic = Topic.objects.get(id = topic_ID)
		topic.active = False
		topic.answer = choice
		user_bets = Player_Topic.objects.filter(topic_id = topic_ID)
		topic.save()
		for obj in user_bets:
			obj.checked = True
			player = Player.objects.get(user_id = obj.user_id)
			if obj.choice == choice:
				player.totalwin += 1
				if not choice:
					player.money += obj.bet*topic.rate1
				else:
					player.money += obj.bet*topic.rate2
			obj.save()
			player.percent = (player.totalwin / player.totalgame)*100
			player.save()
		return HttpResponseRedirect('/edit/')

	form = searchForm(request.GET)
	topics = Topic.objects.filter(due__gte=datetime.now(), active=True).order_by('due')
	if 'title' in request.GET:
		title = request.GET['title']
		topics = topics.filter(title__icontains=title)
	return render(request, 'edit.html', {'topics': topics, 'form': form})






