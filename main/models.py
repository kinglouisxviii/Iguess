from django.db import models

# Create your models here.
class Player(models.Model):
	"""docstring for User"""
	email = models.EmailField()
	username = models.CharField(max_length = 16)
	times_today = models.IntegerField()
	totalwin = models.IntegerField()
	totalgame = models.IntegerField()
	percent = models.FloatField()
	money = models.IntegerField()
	user_id = models.IntegerField()
	last_reg = models.DateField()

class Topic(models.Model):
	"""docstring for Topic"""
	title = models.CharField(max_length = 40)
	due = models.DateTimeField()
	answer = models.BooleanField()
	description = models.TextField()
	option1 = models.CharField(max_length = 100)
	option2 = models.CharField(max_length = 100)
	rate1 = models.FloatField()
	rate2 = models.FloatField()
	active = models.BooleanField(default = True)
	people1 = models.IntegerField(default = 0)
	people2 = models.IntegerField(default = 0)

class Player_Topic(models.Model):
	"""docstring for Topic"""
	user_id = models.IntegerField()
	topic_id = models.IntegerField()
	choice = models.BooleanField()
	bet = models.IntegerField()
	checked = models.BooleanField(default = False)
