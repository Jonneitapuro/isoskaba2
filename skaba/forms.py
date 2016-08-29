from django import forms
from skaba.models import Guild, UserProfile, Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'slug', 'date', 'points', 'guild', 'repeats']

    name = forms.CharField(label='Event name', max_length=128, min_length=1)
    description = forms.CharField(label='Description')
    guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
    date = forms.DateField(widget=forms.SelectDateWidget())
    repeats = forms.IntegerField(label='Repeats', initial=1, min_value=0)
    points = forms.IntegerField(label='Points', min_value=0)

class AddUserForm(UserCreationForm):
    #role choices
    role_choices = (('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin'))
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    #role = forms.CharField(label='User\'s role', required=False, initial='user')
    role = forms.ChoiceField(choices=role_choices)
    guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
    is_kv = forms.BooleanField(required=False)
    is_tf = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_kv', 'is_tf', 'role')

    def save(self,commit = True):
        user = super(AddUserForm, self).save(commit = True)
        user_profile = user.profile
        user_profile.role = self.cleaned_data['role']
        user_profile.guild = self.cleaned_data['guild']
        user_profile.is_kv = self.cleaned_data['is_kv']
        user_profile.is_tf = self.cleaned_data['is_tf']
        user_profile.save()
        return user, user_profile

        if commit:
            user.save()
            return user

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class AdminEditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def save(self, commit = True):
        profile = super(AdminEditProfileForm, self).save(commit = False)
        profile.role = self.cleaned_data['role']
        profile.guild = self.cleaned_data['guild']
        profile.is_kv = self.cleaned_data['is_kv']
        profile.is_tf = self.cleaned_data['is_tf']
        return profile

        if commit:
            profile.save()

        return profile

class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(AdminEditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
