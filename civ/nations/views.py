from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def index(request):
	template = "nations/home.html"
	context = {}
	return render(request,template,context)

def nation(request, nation_id):
    response = "You're looking at nation %s."
    return HttpResponse(response % nation_id)
