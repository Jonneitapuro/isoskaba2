from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.context_processors import csrf
from django.contrib.auth.models import User

from skaba.models import Event
# from skaba.forms import AddEventForm


def index(request):
    response = TemplateResponse(request, 'index.html', {})
    response.render()
    return response

@staff_member_required
def list_users(request):
    """
    Lists all users. Available only for admins.
    """
    users = User.objects.all()
    response = TemplateResponse(request, 'userlist.html', {'users': users})
    response.render()
    return response

@staff_member_required
def list_events(request):
    """
    Lists all events. Available only for admins.
    """
    events = Event.objects.all()
    response = TemplateResponse(request, 'eventlist.html', {'events': events})
    response.render()
    return response

@staff_member_required
def admin_index(request):
    response = TemplateResponse(request, 'admin_index.html', {})
    response.render()
    return response

@staff_member_required
def event_add(request):
	if request.method == 'POST':
		form = addEventForm(request.POST)
		if (form.is_valid()):
			name = request.POST.get('name')
			description = request.POST.get('description')
			slug = request.POST.get('slug')
			points = request.POT.get('points')
			guild = request.POST.get('guild')

			try:
				event = Event(name=name, description=description, slug=slug, points=points, guild=guild)
				event.save()
				status = 200
				return redirect('/admin/events/add', message='event added')
			except:
				status = 400

	else:
		form = AddEventForm()
		status = 200

	token = {}
	token.update(csrf(request))
	token['form'] = form

	return render_to_response('event_add.html', token)
