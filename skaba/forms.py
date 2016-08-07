from django import forms
from skaba.models import Guild, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddEventForm(forms.Form):
	name = forms.CharField(label='Event name', max_length=128, min_length=1)
	description = forms.CharField(label='Description')
	slug = forms.SlugField(label='Slug (used in URL)')
	points = forms.IntegerField(label='Points')
	repeats = forms.IntegerField(label='Repeats')
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)

class AddUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
	role = forms.CharField(label='User\'s role')
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
	is_kv = forms.BooleanField()
	is_tf = forms.BooleanField()

	class Meta:
        model = User
        fields = ('email', 'password1')

    def save(self,commit = True):
        user = super(AddUserForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first name']
        user.last_name = self.cleaned_data['last name']
		user.role = self.cleaned_data['role']
		user.guild = self.cleaned_data['guild']
		user.is_kv = self.cleaned_data['is_kv']
		user.is_tf = self.cleaned_data['is_tf']


        if commit:
            user.save()
			return user
