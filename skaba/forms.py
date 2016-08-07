from django import forms
from skaba.models import Guild, User

class AddEventForm(forms.Form):
	name = forms.CharField(label='Event name', max_length=128, min_length=1)
	description = forms.CharField(label='Description')
	slug = forms.SlugField(label='Slug (used in URL)')
	points = forms.IntegerField(label='Points')
	repeats = forms.IntegerField(label='Repeats')
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)

class AddUserForm(forms.Form):
	email = forms.CharField(label='User e-mail', max_length=128, min_length=1)
	real_name = forms.CharField(label='Full name')
	role = forms.CharField(label='User\'s role')
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
	is_kv = forms.BooleanField()
	is_tf = forms.BooleanField()
