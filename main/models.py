from django.db import models

# Create your models here.
class User(models.Model):
	"""docstring for User"""
	email = models.EmailField()
	username = models.CharField(max_length = 16)
	times_today = models.IntegerField()
	password = models.CharField(max_length = 40)
	totalwin = models.IntegerField()
	totalgame = models.IntegerField()
	percent = models.FloatField()

class Topic(models.Model):
	"""docstring for Topic"""
	ditle = models.CharField(max_length = 40)
	due = models.DateTimeField()
	reward = models.IntegerField()
	answer = models.BooleanField()
	whom = models.CharField(max_length = 16)
	description = models.TextField()
	option1 = models.CharField(max_length = 100)
	option2 = models.CharField(max_length = 100)

class User_Topic(models.Model):
	"""docstring for Topic"""
	user_id = models.IntegerField()
	topic_id = models.IntegerField()
	choice = models.BooleanField()
