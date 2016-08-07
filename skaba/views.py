from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.context_processors import csrf
from django.contrib.auth.models import User

from skaba.forms import AddEventForm
from skaba.models import Event, Guild


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
		form = AddEventForm(request.POST)
		if (form.is_valid()):
			name = request.POST.get('name')
			description = request.POST.get('description')
			slug = request.POST.get('slug')
			points = request.POST.get('points')
			guild = Guild.objects.get(pk=request.POST.get('guild'))

			try:
				event = Event(name=name, description=description, slug=slug, points=points, guild=guild)
				event.save()
				status = 200
				messages.add_message(request, messages.INFO, 'event added')
				return redirect('/admin/events/add')
			except:
				status = 400

	else:
		form = AddEventForm()
		status = 200

	token = {}
	token.update(csrf(request))
	token['form'] = form
	token['site_title'] = 'Create event'
	token['submit_text'] = 'Add event'
	token['form_action'] = '/admin/events/add'

	return render_to_response('admin_form.html', token)

@staff_member_required
def guilds_populate(request):
	if Guild.objects.all().exists():
		return redirect('index')
	guilds = [
		{'name': 'Yleinen', 'abbr': 'Yleinen'},
		{'name': 'Arkkitehtikilta', 'abbr': 'AK'},
		{'name': 'AS-kilta', 'abbr': 'AS'},
		{'name': 'Athene', 'abbr': 'Athene'},
		{'name': 'Fyysikkokilta', 'abbr': 'FK'},
		{'name': 'Inkubio', 'abbr': 'Bio'},
		{'name': 'Koneinsinöörikilta', 'abbr': 'KIK'},
		{'name': 'Maanmittarikilta', 'abbr': 'MK'},
		{'name': 'Prodeko', 'abbr': 'Prodeko'},
		{'name': 'Prosessiteekkarit', 'abbr': 'PT'},
		{'name': 'Rakennusinsinöörikilta', 'abbr': 'IK'},
		{'name': 'Sähköinsinöörikilta', 'abbr': 'SIK'},
		{'name': 'Tietokilta', 'abbr': 'TiK'},
		{'name': 'Teknologföreningen', 'abbr': 'TF'}
	]
	for guild in guilds:
		new_guild = Guild(name=guild['name'], abbreviation = guild['abbr'])
		new_guild.save()
	return redirect('index')
