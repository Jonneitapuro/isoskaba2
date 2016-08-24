from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.template.context_processors import csrf
from django.forms import model_to_dict
from django.db.models import Q

from skaba.forms import EventForm, AddUserForm
from skaba.models import Event, Guild, User, UserProfile
from skaba.util import check_moderator, check_admin

def index(request):
	response = TemplateResponse(request, 'index.html', {})
	response.render()
	return response

@user_passes_test(check_moderator)
def list_users(request):
	"""
	Lists all users. Available only for admins.
	"""
	order_by = request.GET.get('order_by', 'username')
	users = User.objects.all().order_by(order_by)
	response = TemplateResponse(request, 'userlist.html', {'users': users})
	response.render()
	return response

@user_passes_test(check_moderator)
def list_events(request):
	"""
	Lists all events. Available only for admins.
	"""
	order_by = request.GET.get('order_by', 'name')
	events = Event.objects.all().order_by(order_by)
	response = TemplateResponse(request, 'admin_eventlist.html', {'events': events})
	response.render()
	return response

@user_passes_test(check_moderator)
def admin_index(request):
	response = TemplateResponse(request, 'admin_index.html', {})
	response.render()
	return response

@user_passes_test(check_moderator)
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if (form.is_valid()):
            try:
                form.save()
                status = 200
                messages.add_message(request, messages.INFO, 'event added')
                return redirect('/admin/events/add/')
            except:
                status = 400

    else:
        form = EventForm()
        status = 200

    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['site_title'] = 'Create event'
    token['submit_text'] = 'Add event'
    token['form_action'] = '/admin/events/add/'

    return render(request, 'admin_form.html', token)

@user_passes_test(check_moderator)
def event_edit(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if (form.is_valid()):
            try:
                form.save()
                status = 200
                messages.add_message(request, messages.INFO, 'event saved')
                return redirect('/admin/events/edit/' + slug + '/')
            except:
                status = 400

    else:
        form = EventForm(instance=event)
        status = 200

    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['site_title'] = 'Edit event'
    token['submit_text'] = 'Save event'
    token['form_action'] = '/admin/events/edit/' + event.slug + '/'

    return render(request, 'admin_form.html', token)

@user_passes_test(check_admin)
def guilds_populate(request):
	if Guild.objects.all().exists():
		return redirect('index')
	guilds = [
		{'name': 'Yleinen', 'abbr': 'Yleinen'},
		{'name': 'Arkkitehtikilta', 'abbr': 'AK'},
		{'name': 'Automaatio- ja systeemitekniikan kilta', 'abbr': 'AS'},
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

@user_passes_test(check_moderator)
def user_add(request):
	if request.method == 'POST':
		form = AddUserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.INFO, 'Creation successfull')
			return redirect('/admin/users/add')
	else:
		form = AddUserForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	args['site_title'] = 'Add User'
	args['submit_text'] = 'Add user'
	args['form_action'] = '/admin/users/add'
	return render(request, 'admin_form.html', args)

def login_user(request):
    c = RequestContext(request)
    redirectURL = request.GET.get('next', None)

    if (request.user and request.user.is_authenticated()):
        return redirect('index')

    username = password = ''
    status = 200

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirectURL = request.POST.get('next')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Logged in successfully, welcome ' + username)
                if redirectURL is not None and redirectURL != 'None':
                    return redirect(redirectURL)
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Your account is not active.')
                status=403 #Forbidden
        else:
            messages.error(request, 'Invalid username and/or password.')
            status=401 #Unauthorised


    return render(request, 'simple_login.html', {'username': username, 'next': redirectURL}, c, status=status)

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('index')

def list_user_events(request):
    order_by = request.GET.get('order_by', 'guild')
    cur_user = request.user
    cur_user_profile = UserProfile.objects.get(user_id = cur_user.id)
    if cur_user_profile.is_tf == 1:
        tf = 14
    else:
        tf = 20
    events = Event.objects.filter(Q(guild__id = cur_user_profile.guild_id) | Q(guild__id = 1) | Q(guild__id = tf)).order_by(order_by)
    response = TemplateResponse(request, 'eventlist.html', {'events': events})
    response.render()
    return response
