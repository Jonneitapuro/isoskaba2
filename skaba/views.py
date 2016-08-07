from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.context_processors import csrf

from skaba.forms import AddEventForm
from skaba.models import Event, Guild, User

# Create your views here.

def index(request):
    response = TemplateResponse(request, 'index.html', {})
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

	return render_to_response('event_add.html', token)

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

@staff_member_required
def user_add(request):
	if request.method == 'POST':
		form = AddUserForm(request.POST)
		if (form.is_valid()):
			email = request.POST.get('email')
			real_name = request.POST.get('real_name')
            role = request.POST.get('role')
			guild = Guild.objects.get(pk=request.POST.get('guild'))
            is_tf = request.POST.get('is_tf')
            is_kv = request.POST.get('is_kv')

			try:
				user = User(email=email, real_name=real_name, role=role, guild=guild, is_kv=is_kv, is_tf=is_tf)
				user.save()
				status = 200
				messages.add_message(request, messages.INFO, 'user added')
				return redirect('/admin/users/add')
			except:
				status = 400

	else:
		form = AddUserForm()
		status = 200

	token = {}
	token.update(csrf(request))
	token['form'] = form

	return render_to_response('user_add.html', token)
