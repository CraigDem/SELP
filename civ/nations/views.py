from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from nations.forms import UserForm, NationForm
from nations.models import Nation
from django.contrib.auth.models import User
from django.views.generic import View, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelFormSet
import random

class indexView(View):
    def get(self, request):
    	return render(request,'nations/home.html',{})

class nationView(DetailView):
    model = Nation

class editNationView(UpdateView, ModelFormMixin):
   
    model = Nation
    form_class = NationForm


    def get(self, request, pk):
        context = RequestContext(request)
        nation = Nation.objects.get(pk=pk)
        nation_form = NationForm(instance=nation)
        return render_to_response('nations/nation_form.html',{'form': nation_form, 'nation': nation},context)

    def post(self, request, pk):
        context = RequestContext(request)
        nation = Nation.objects.get(pk=pk)
        nation_form = NationForm(data=request.POST, instance=nation)
        if nation_form.is_valid():
            nation_form.save()
            return redirect('/nation/' + pk)
        return render_to_response('nations/nation_form.html',{'form_errors': nation_form.errors, 'nation':nation},context)

class registerView(View):
    
    registered = False

    def get(self, request):
        context = RequestContext(request)
        user_form = UserForm()
        return render_to_response('registration/register.html',{'user_form': user_form, 'registered': self.registered}, context)

    def post(self, request):
        context = RequestContext(request)
        user_form = UserForm(data=request.POST)
        resources = random.sample(set(['Aluminium','Cattle','Coal','Fish','Furs','Gold','Gems','Iron','Lead','Lumber','Marble','Oil','Pigs','Rubber','Silver','Spices','Sugar','Uranium','Water','Wheat','Wine']),2)
        
        if user_form.is_valid():
            user = User.objects.create_user(username=user_form['username'].value(), password='')
            user.set_password(user_form['password'].value())
            user.save()
            Nation.objects.create(nation_name=user_form['nation_name'].value(),user=user,resource1=resources[0],resource2=resources[1])

            registered = True

        else:
            registered = False
            print user_form.errors

        return render_to_response('registration/register.html',{'user_form': user_form, 'registered': registered}, context)
