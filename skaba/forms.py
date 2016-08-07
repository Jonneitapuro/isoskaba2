from django import forms
from skaba.models import Guild

class AddEventForm(forms.Form):
	name = forms.CharField(label='Event name', max_length=128, min_length=1)
	description = forms.CharField(label='Description')
	slug = forms.SlugField(label='Slug (used in URL)')
	points = forms.IntegerField(label='Points')
	guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)