from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.context_processors import csrf
from django.forms import model_to_dict

from skaba.forms import EventForm, AddUserForm
from skaba.models import Event, Guild, User

def index(request):
    response = TemplateResponse(request, 'index.html', {})
    response.render()
    return response

@staff_member_required
def list_users(request):
    """
    Lists all users. Available only for admins.
    """
    order_by = request.GET.get('order_by', 'real_name')
    users = User.objects.all().order_by(order_by)
    response = TemplateResponse(request, 'userlist.html', {'users': users})
    response.render()
    return response

@staff_member_required
def list_events(request):
    """
    Lists all events. Available only for admins.
    """
    order_by = request.GET.get('order_by', 'name')
    events = Event.objects.all().order_by(order_by)
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

    return render_to_response('admin_form.html', token)

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

@staff_member_required
def user_add(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if (form.is_valid()):
            role = request.POST.get('role')
            email = request.POST.get('email')
            real_name = request.POST.get('real_name')
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
    token['site_title'] = 'Add User'
    token['submit_text'] = 'Add user'
    token['form_action'] = '/admin/users/add'

    return render_to_response('admin_form.html', token)
