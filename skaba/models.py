from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class User(models.Model):
	email = models.CharField(max_length=40, unique=True)
	real_name = models.CharField(max_length=40)
	is_tf = models.BooleanField(default=False)
	is_kv = models.BooleanField(default=False)
	role = models.CharField(max_length=8, default="user")
	guild = models.ForeignKey('Guild', on_delete=models.CASCADE)

# This bit of code is copy-pasted from a previous project.
# Not sure what it does ¯\_(ツ)_/¯
# Might be useful/required though
# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
#
# # catch user creation
# def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
#
# post_save.connect(create_user_profile, sender=User)


class Guild(models.Model):
        name = models.CharField(max_length=64)
        abbreviation = models.CharField(max_length=8)

        def __str__(self):
                return u'{0}'.format(self.name)

class Event(models.Model):
	name = models.TextField()
	description = models.TextField()
	slug = models.SlugField(unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	date = models.DateField()
	points = models.IntegerField(default=1)
	repeats= models.IntegerField(default=1)
	guild = models.ForeignKey('Guild', on_delete=models.CASCADE)

class Attendance(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField()
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
