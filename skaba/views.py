from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse


# Create your views here.

def index(request):
    response = TemplateResponse(request, 'index.html', {})
    response.render()
    return response