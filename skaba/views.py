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

from datetime import datetime, date, timedelta
from skaba.forms import *
from skaba.models import Event, Guild, User, UserProfile, Attendance, Guildpoints
from skaba.util import check_moderator, check_admin, csv_user_import, csv_event_import

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
	if check_moderator:
		users = User.objects.filter(userprofile__guild = request.user.userprofile.guild).order_by(order_by)
	if check_admin:
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
    token['forms'] = [form]
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
    token['forms'] = [form]
    token['site_title'] = _('Edit event')
    token['submit_text'] = _('Save event')
    token['form_action'] = '/admin/events/edit/' + event.slug + '/'

    return render(request, 'admin_form.html', token)

@user_passes_test(check_moderator)
def fix_events(request):
    e = Event.objects.all()
    for i in e:
        i.slug = i.slug.replace('_','-')
        i.save()
    return redirect('index')

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

@user_passes_test(check_admin)
def guild_points_populate(request):
    if Guildpoints.objects.all().exists():
        return redirect('index')
    guilds = Guild.objects.all()
    for guild in guilds:
        if guild.id != 1 and guild.id != 14:
            new_guild = Guildpoints(guild=guild, points = 0)
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
	args['forms'] = [form]
	args['site_title'] = _('Add User')
	args['submit_text'] = _('Add user')
	args['form_action'] = '/admin/users/add'
	return render(request, 'admin_form.html', args)

def user_import(request):
    if request.method == 'POST':
        form = ImportUserForm(request.POST, request.FILES)
        if form.is_valid():
            if csv_user_import(request.FILES['csv_file'], request.POST.get('guild')):
                messages.success(request, _('Import successful'))
            else:
                messages.error(request, _('Import failed'))
            return redirect('/admin/users/')
    else:
        form = ImportUserForm()

    args = {}
    args.update(csrf(request))
    args['forms'] = [form]
    args['site_title'] = _('Import users')
    args['submit_text'] = _('Import')
    args['form_action'] = '/admin/users/import'
    return render(request, 'admin_form.html', args)

def event_import(request):
    if request.method == 'POST':
        form = ImportEventForm(request.POST, request.FILES)
        if form.is_valid():
            if csv_event_import(request.FILES['csv_file'], request.POST.get('guild')):
                messages.success(request, _('Import successful'))
            else:
                messages.error(request, _('Import failed'))
            return redirect('/admin/events/')
    else:
        form = ImportEventForm()

    args = {}
    args.update(csrf(request))
    args['forms'] = [form]
    args['site_title'] = _('Import events')
    args['submit_text'] = _('Import')
    args['form_action'] = '/admin/events/import'
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
                messages.success(request, _('Logged in successfully, welcome') + ' ' + username)
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
    order_by_events = request.GET.get('order_by_events', 'guild')
    order_by_attendances = request.GET.get('order_by_attendances', 'verified')
    cur_user = request.user
    cur_user_profile = UserProfile.objects.get(user_id  = cur_user.id)
    if cur_user_profile.is_tf == 1:
        tf = 14
    else:
        tf = 20
    events = Event.objects.filter(Q(guild__id = cur_user_profile.guild_id) | Q(guild__id = 1) | Q(guild__id = tf)).order_by(order_by_events)
    attendances = Attendance.objects.filter(Q(user__id = request.user.pk)).order_by(order_by_attendances)
    for event in events:
        if attendances.filter(event=event.pk).count() >= event.repeats:
            events = events.exclude(pk=event.pk)

    response = TemplateResponse(request,
            'eventlist.html',
            {
                'events': events, 'attendances': attendances,
                'order_by_attendances': order_by_attendances,
                'order_by_events': order_by_events
            })

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
    # TODO: reformat redirection
    if 'e_id' in request.POST:
        response = redirect('usereventlist')
        response['Location'] += '?order_by_attendances=' + \
                request.POST.get('order_by_attendances', 'verified') + \
                '&order_by_events=' + \
                request.POST.get('order_by_events', 'guild')

        eventid = int(request.POST.get('e_id'))
        event = get_object_or_404(Event, pk=eventid)
        cur_user = UserProfile.objects.get(user_id = request.user.id)
        repcount = Attendance.objects.filter(Q(user_id = cur_user.id) & Q(event_id = eventid)).count()
        if  event.repeats > repcount:
            a = Attendance(event_id = eventid, user_id = cur_user.id)
            a.save()
            return response
        else:
            messages.error(request, _('You have attended for the maximum amount'))
            return response
    else:
        return redirect('usereventlist')

@user_passes_test(check_moderator)
def verify_attendances(request):

    if 'attendance' in request.POST:
        attendance = Attendance.objects.get(pk=request.POST.get('attendance'))
        attendance.verified = True
        attendance.save()

    if 'delete' in request.POST:
        attendance = Attendance.objects.get(pk=request.POST.get('delete'))
        attendance.delete()

    order_by = request.GET.get('order_by', 'user')
    guild_users = User.objects.filter(userprofile__guild = request.user.userprofile.guild)
    unverified = Attendance.objects.filter(Q(user__in = guild_users) & Q(verified = False)).order_by(order_by)
    verified = Attendance.objects.filter(Q(user__in = guild_users) & Q(verified = True)).order_by(order_by)

    response = TemplateResponse(request, 'admin_attendances.html', {'unverified': unverified, 'verified': verified})
    response.render()
    return response

@user_passes_test(check_admin)
def delete_user(request):
    if 'user_id' in request.POST:
        userid = int(request.POST.get('user_id'))
        "user = get_object_or_404(user, pk=userid)"
        User.objects.filter(id = userid).delete()
        return redirect('userlist')
    else:
        messages.error(request, _('Something went wrong!'))
        return redirect('userlist')

@user_passes_test(check_moderator)
def delete_event(request):
    if 'event_id' in request.POST:
        eventid = int(request.POST.get('event_id'))
        Event.objects.filter(id = eventid).delete()
        return redirect('eventlist')
    else:
        messages.error(request, _('Something went wrong!'))
        return redirect('eventlist')

def guild_ranking(request):
    order_by = request.GET.get('order_by', 'points')
    points = Guildpoints.objects.all().order_by(order_by).reverse()
    response = TemplateResponse(request, 'guildrank.html', {'points':points})
    return response

@user_passes_test(check_moderator)
def guild_points_update(request):
    guilds = Guildpoints.objects.all()
    n = 0
    users = User.objects.filter(userprofile__role = 'user')
    attendances = Attendance.objects.filter(verified = True)
    events = Event.objects.filter(eventdate__lte= date.today())
    for g in guilds:
        guild_users = []
        for user in users: #list user of the guild
            if user.profile.guild_id == g.guild_id:
               guild_users.append(user)
        usercount = len(guild_users)
        useravg = 0.5 * usercount
        useravg = int(useravg)
        guild_list = []
        general_list = []
        guildatts = 0
        for user in guild_users: #list attendances
            user_attendances = []
            for attendance in attendances: 
                if attendance.user_id == user.id:
                    user_attendances.append(attendance)
            guipoints = 0
            genpoints = 0
            for att in user_attendances: #go through attendances
                event = 0
                for e in events: #crossreference to events
                    if e.id == att.event_id:
                        event = e
                if event is not 0:
                    try:
                        if event.guild_id == g.guild_id: #add guild eventpoints
                            guildatts = guildatts + 1
                            addpoints = event.points
                            addpoints = int(addpoints)
                            guipoints = guipoints + addpoints
                        if event.guild_id == 1: #add general eventpoints
                            addpoints = event.points
                            addpoints = int(addpoints)
                            genpoints = genpoints + addpoints
                    except (UnboundLocalError):
                        pass
            guild_list.append(guipoints)
            general_list.append(genpoints)
        guild_list = sorted(guild_list)
        general_list = sorted(general_list)
        if len(guild_list) > 0 and len(general_list) > 0: 
            guildpoints = 0
            generalpoints = 0
            count = 0
            for x in range(useravg, usercount):
                count = count + 1
                guildpoints = guildpoints + guild_list[x]
            guildpoints = guildpoints/count
            count = 0
            for x in range(useravg, usercount):
                count = count + 1
                generalpoints = generalpoints + general_list[x]
            generalpoints = generalpoints/count
            guildevents = []                
            genevents = []
            for e in events:
                if e.guild_id == g.guild_id:
                    guildevents.append(e)
                if e.guild_id == 1:
                    genevents.append(e)
            guildpointsum = 0
            genpointsum = 0
            for e in guildevents:
                guildpointsum = guildpointsum + e.points
            for e in genevents:
                genpointsum = genpointsum + e.points
            if guildpointsum is not 0:
                scalingfactor = genpointsum / float(guildpointsum)
            else:
                scalingfactor = 0
            guildpoints = scalingfactor * guildpoints
            guildmaxatts = len(guildevents) * usercount
            if guildatts is not 0:
                guildattendance = guildatts/guildmaxatts
            else:
                guildattendance = 0
            points = 15 * int(guildpoints * guildattendance + generalpoints)
            Guildpoints.objects.filter(guild_id = g.guild_id).update(points = points)
        else: 
            pass
        n = n + 1
    return redirect('guild_ranking')

@login_required
def user_ranking(request):

    users = User.objects.filter(Q(userprofile__guild = request.user.userprofile.guild) & Q(userprofile__role = 'user'))
    score_list = []
    n = 0
    for user in users:
        score_list.append([])
        score_list[n].append(user.first_name)
        score_list[n].append(user.last_name)
        attendances = Attendance.objects.filter(Q(user_id = user.id) & Q(verified = True))
        points = 0
        for att in attendances:
            event = Event.objects.filter(id = att.event_id)
            addpoints = event.points
            addpoints = int(addpoints)
            points = points + addpoints
        score_list[n].append(points)
        n = n + 1
    score_list = sorted(score_list, key=lambda points: points[2], reverse=True)
    response = TemplateResponse(request, 'userrank.html', {'score_list': score_list})
    response.render()
    return response
