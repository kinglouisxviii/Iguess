from django.db import models
from django import forms

# Create your models here.
class User(models.Model):
	"""docstring for User"""
	Email = models.EmailField()
	Name = models.CharField(max_length = 16)
	Times_today = models.IntegerField()
	password = models.CharField(max_length = 40)

class Topic(models.Model):
	"""docstring for Topic"""
	Title = models.CharField(max_length = 40)
	due = models.DateTimeField()
	reward = models.IntegerField()
	answer = models.BooleanField()
	whom = models.CharField(max_length = 16)
	Description = models.TextField()
	option1 = models.CharField(max_length = 100)
	option2 = models.CharField(max_length = 100)

class User_Topic(models.Model):
	"""docstring for Topic"""
	User_id = models.IntegerField()
	Topic_id = models.IntegerField()
	choice = models.BooleanField()
