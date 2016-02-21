from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Access(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Role(models.Model):
	role_choice = [
		('Admin','Admin'),
		('Employee','Employee'),
		('Errand Boy','Errand Boy'),
	]
	role = models.CharField(choices=role_choice, max_length=50)
	access = models.ManyToManyField(Access) 

	def __str__(self):
		return self.role

class MyUser(models.Model):
	user = models.OneToOneField(User, related_name='myuser')
	role = models.ForeignKey(Role)
	location = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username

class Service(models.Model):
	name = models.CharField(max_length=50)
	cost = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class Job(models.Model):
	service = models.ForeignKey(Service)
	quantity = models.IntegerField(default=1)
	assigned = models.ForeignKey(User, related_name='assigned_to')
	time = models.DateTimeField(auto_now_add=True)
	by = models.ForeignKey(User, related_name='job_by')
	granted = models.BooleanField(default=False)
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return self.service.name


