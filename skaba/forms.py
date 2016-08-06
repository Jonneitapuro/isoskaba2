from django import forms
from hashlib import md5
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import UserProfile

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "is_developer")

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['First name']
        user.last_name = self.cleaned_data['Last name']
        user.birthday = self.cleaned_data['Birthday']


        if commit:
            user.save()

        return user
