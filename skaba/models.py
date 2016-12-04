from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_tf = models.BooleanField(default=False)
    is_kv = models.BooleanField(default=False)
    role = models.CharField(max_length=9, default="user")
    guild = models.ForeignKey('Guild', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return u'%s %s' % (self.user.name)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

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
    eventdate = models.DateField()
    points = models.IntegerField(default=1)
    repeats= models.IntegerField(default=1)
    guild = models.ForeignKey('Guild', on_delete=models.CASCADE)

    def __str__(self):
        return u'{0}'.format(self.name)

class Attendance(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	verified = models.BooleanField(default=False)
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Guildpoints(models.Model):
	guild = models.ForeignKey('Guild', on_delete=models.CASCADE, blank=True, null=True)
	points = models.IntegerField(default=1)
