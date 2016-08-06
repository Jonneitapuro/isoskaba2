from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.model):
	user = models.OneToOneField(User)
	is_tf = models.BooleanField(default=False)
        is_kv = models.BooleanField(default=False)
	role = models.CharField(max_length=8, default="user")

# This bit of code is copy-pasted from a previous project.
# Not sure what it does ¯\_(ツ)_/¯
# Might be useful/required though
# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# catch user creation
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
#
#post_save.connect(create_user_profile, sender=User)
#

class Guild(models.Model):
	name = models.CharField(max_length=64)
	abbreviation = models.CharField(max_length=8)

class Events(models.Model):
	name = models.TextField()
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	points = models.IntegerField()
        repeats = models.IntegerField()
	guild = models.ForeignKey('Guild', on_delete=models.CASCADE)

class Attendances(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField()
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)



