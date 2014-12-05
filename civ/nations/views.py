from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def index(request):
	template = loader.get_template('nations/home.html')
	return HttpResponse(template)

def nation(request, nation_id):
    response = "You're looking at nation %s."
    return HttpResponse(response % nation_id)
