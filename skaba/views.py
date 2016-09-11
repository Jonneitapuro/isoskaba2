from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from django.forms import model_to_dict
from django.utils.translation import ugettext as _
from django.db.models import Q, Count, Sum

from skaba.forms import *
from skaba.models import Event, Guild, User, UserProfile, Attendance
from skaba.util import check_moderator, check_admin

def index(request):
    response = TemplateResponse(request, 'index.html', {})
    response.render()
    print(request.LANGUAGE_CODE)
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
                messages.add_message(request, messages.INFO, _('Event added'))
                return redirect('/admin/events/add/')
            except:
                status = 400

    else:
        form = EventForm()
        status = 200

    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['site_title'] = _('Create event')
    token['submit_text'] = _('Add event')
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
                messages.add_message(request, messages.INFO, _('Event saved'))
                return redirect('/admin/events/edit/' + slug + '/')
            except:
                status = 400

    else:
        form = EventForm(instance=event)
        status = 200

    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['site_title'] = _('Edit event')
    token['submit_text'] = _('Save event')
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
			messages.add_message(request, messages.INFO, _('Creation successfull'))
			return redirect('/admin/users/add')
	else:
		form = AddUserForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	args['site_title'] = _('Add User')
	args['submit_text'] = _('Add user')
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
                messages.success(request, _('Logged in successfully, welcome ') + username)
                if redirectURL is not None and redirectURL != 'None':
                    return redirect(redirectURL)
                else:
                    return redirect('index')
            else:
                messages.error(request, _('Your account is not active.'))
                status=403 #Forbidden
        else:
            messages.error(request, _('Invalid username and/or password.'))
            status=401 #Unauthorised


    return render(request, 'simple_login.html', {'username': username, 'next': redirectURL, 'view': 'login'}, c, status=status)

def logout_user(request):
    logout(request)
    messages.success(request, _('Logged out'))
    return redirect('index')

@login_required
def list_user_events(request):
    order_by = request.GET.get('order_by', 'guild')
    cur_user = request.user
    cur_user_profile = UserProfile.objects.get(user_id  = cur_user.id)
    if cur_user_profile.is_tf == 1:
        tf = 14
    else:
        tf = 20
    events = Event.objects.filter(Q(guild__id = cur_user_profile.guild_id) | Q(guild__id = 1) | Q(guild__id = tf)).order_by(order_by)
    response = TemplateResponse(request, 'eventlist.html', {'events': events})
    response.render()
    return response

@login_required
def user_info(request):
    cur_user = request.user	
    cur_user_profile = UserProfile.objects.get(user_id = cur_user.id)
    attendances = Attendance.objects.filter(user = cur_user)
    response = TemplateResponse(request, 'user_info.html', {'profile': cur_user_profile, 'attendances': attendances})
    response.render()
    return response

@login_required
def user_edit(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if (form.is_valid()):
            try:
                form.save()
                status = 200
                messages.add_message(request, messages.INFO, 'Changes saved')
                return redirect('/user/edit/')
            except:
                status = 400

    else:
        form = EditUserForm(instance=request.user)
        status = 200

    token = {}
    token.update(csrf(request))
    token['forms'] = [form]
    token['site_title'] = 'Edit user info'
    token['submit_text'] = 'Save user info'
    token['form_action'] = '/user/edit/'

    return render(request, 'form.html', token)

@user_passes_test(check_moderator)
def admin_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = user.profile
    if request.method == "POST":
        user_form = AdminEditUserForm(request.POST, instance=user)
        profile_form = AdminEditProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save()
                profile_form.save()
                status = 200
                messages.add_message(request, messages.INFO, 'Changes saved')
                return redirect('/admin/users/edit/' + user_id + '/')
            except:
                status = 400

    else:
        user_form = AdminEditUserForm(instance=user)
        profile_form = AdminEditProfileForm(instance=profile)
        status = 200

    token = {}
    token.update(csrf(request))
    token['forms'] = [user_form, profile_form]
    token['site_title'] = 'Edit user info'
    token['submit_text'] = 'Save user info'
    token['form_action'] = '/admin/users/edit/' + user_id + '/'

    return render(request, 'admin_form.html', token)

def attend_event(request):
    if 'attend' in request.POST:
        reps = request.POST.get('e_repeats')
        reps = int(reps)
        eventid = request.POST.get('e_id')
        eventid = int(eventid)
        cur_user = UserProfile.objects.get(user_id = request.user.id)
        repcount = Attendance.objects.filter(Q(user_id = cur_user.id) & Q(event_id = request.POST.get('e_id'))).count()
        if  reps > repcount:
            a = Attendance(event_id = eventid, user_id = cur_user.id)
            a.save()
            return redirect('usereventlist')
        else:
            messages.error(request, _('You have attended for the maximum amount'))
            return redirect('usereventlist')

def verify_attendances(request):

    if request.POST:
        attendance = Attendance.objects.get(pk=request.POST.get('attendance'))
        attendance.verified = True
        attendance.save()

    order_by = request.GET.get('order_by', 'user')
    guild_users = User.objects.filter(userprofile__guild = request.user.userprofile.guild)
    unverified = Attendance.objects.filter(Q(user__in = guild_users) & Q(verified = False)).order_by(order_by)
    verified = Attendance.objects.filter(Q(user__in = guild_users) & Q(verified = True)).order_by(order_by)

    response = TemplateResponse(request, 'admin_attendances.html', {'unverified': unverified, 'verified': verified})
    response.render()
    return response

def guild_ranking(request):
    guilds = Guild.objects.all()
    score_list = []
    n = 0
    for guild in guilds:
        score_list.append([])
        score_list[n].append(guild.name)
        users = User.objects.filter(userprofile__guild = request.user.userprofile.guild)
        attendances = Attendance.objects.filter(user__in = users)
        points = 0
        for att in attendances:
            event = Event.objects.get(id = att.event_id)
            addpoints = event.points
            addpoints = int(addpoints)
            points = points + addpoints
        score_list[n].append(points)
        n = n + 1
    response = TemplateResponse(request, 'guildrank.html', {'score_list': score_list})
    response.render()
    return response

