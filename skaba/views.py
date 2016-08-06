from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib import auth
from django.core.context_processors import csrf
from forms import UserRegistrationForm


def index(request):
    response = TemplateResponse(request, 'index.html', {})
    response.render()
    return response


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
    args = {}
    args.update(csrf(request))
    args['form'] = MyRegistrationForm()
    print args
    return render(request, 'register.html', args)
