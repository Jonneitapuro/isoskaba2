from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from skaba.models import Event
from skaba.util import check_admin


def index(request):
    response = TemplateResponse(request, 'index.html', {})
    response.render()
    return response

# @login_required
# @user_passes_test(check_admin)
@staff_member_required
def list_users(request):
    """
    Lists all users. Available only for admins.
    """
    users = User.objects.all()
    response = TemplateResponse(request, 'userlist.html', {'users': users})
    response.render()
    return response

# @login_required
# @user_passes_test(check_admin)
@staff_member_required
def list_events(request):
    """
    Lists all events. Available only for admins.
    """
    events = Event.objects.all()
    response = TemplateResponse(request, 'eventlist.html', {'events': events})
    response.render()
    return response
