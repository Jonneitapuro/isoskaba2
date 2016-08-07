from django import forms
from skaba.models import Guild, User, Event

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'description', 'slug', 'date', 'points', 'guild', 'repeats']
	
	name = forms.CharField(label='Event name', max_length=128, min_length=1)
	description = forms.CharField(label='Description')
	date = forms.DateField(widget=forms.SelectDateWidget)
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
	repeats = forms.IntegerField(label='Repeats', initial=1, min_value=0)
	points = forms.IntegerField(label='Points', min_value=0)

class AddUserForm(forms.Form):
	email = forms.CharField(label='User e-mail', max_length=128, min_length=1)
	real_name = forms.CharField(label='Full name')
	role = forms.CharField(label='User\'s role')
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
	is_kv = forms.BooleanField()
	is_tf = forms.BooleanField()
