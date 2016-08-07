from django import forms
from skaba.models import Guild, Event

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'description', 'slug', 'points', 'guild']
	
	name = forms.CharField(label='Event name', max_length=128, min_length=1)
	description = forms.CharField(label='Description')
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)