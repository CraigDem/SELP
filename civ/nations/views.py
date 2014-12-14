from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from nations.forms import UserForm, NationForm, extendForm
from nations.models import Nation
from django.contrib.auth.models import User
from django.views.generic import View, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelFormSet
from decimal import Decimal
import datetime
from django.utils import timezone
import random

class indexView(View):
    def get(self, request):
    	return render(request,'nations/home.html',{})

class noEntry(View):
    def get(self, request):
        return render(request,'nations/error.html',{})

class registerView(View):
    
    registered = False

    def get(self, request):
        user_form = UserForm()
        return render_to_response('registration/register.html',{'user_form': user_form, 'registered': self.registered}, RequestContext(request))

    def post(self, request):
        user_form = UserForm(data=request.POST)
        resources = random.sample(set(['Aluminium','Cattle','Coal','Fish','Furs','Gold','Gems','Iron','Lead','Lumber','Marble','Oil','Pigs','Rubber','Silver','Spices','Sugar','Uranium','Water','Wheat','Wine']),2)
        
        if user_form.is_valid():
            user = User.objects.create_user(username=user_form['username'].value(), password='')
            user.set_password(user_form['password'].value())
            user.save()
            Nation.objects.create(nation_name=user_form['nation_name'].value(),user=user,resource1=resources[0],resource2=resources[1],paid_bills=timezone.now())

            registered = True

        else:
            registered = False
            print user_form.errors

        return render_to_response('registration/register.html',{'user_form': user_form, 'registered': registered},RequestContext(request))


class nationView(DetailView):
    model = Nation

class editNationView(UpdateView, ModelFormMixin):
   
    model = Nation
    form_class = NationForm

    def get(self, request, pk):
        nation = Nation.objects.get(pk=pk)

        if request.user != nation.user:
            return redirect('noEntry')
        else:   
            return render_to_response('nations/nation_form.html',{'form': NationForm(instance=nation), 'nation': nation},RequestContext(request))

    def post(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        if request.user != nation.user:
            return redirect('noEntry')
        else:
            nation_form = NationForm(data=request.POST, instance=nation)
            if nation_form.is_valid():
                nation_form.save()
                return redirect('/nation/' + pk)
            return render_to_response('nations/nation_form.html',{'form_errors': nation_form.errors, 'nation':nation},RequestContext(request))

class expandNationView(UpdateView, ModelFormMixin):

    model = Nation
    form_class = extendForm

    def calculate_cost(self,level,amount):
        if amount == 0:
            cost = 0
        elif amount > 0:
            if level < 100:
                cost = 100 * amount
            elif level >= 100 and level < 1000:
                cost = 200 * amount
            elif level >= 1000 and level < 2000:
                cost = 400 * amount
            elif level >= 2000 and level < 3000:
                cost = 800 * amount
            else:
                cost = 1000 * amount
        else:
            cost = 5 * amount

        return cost

    def get(self, request, pk):  
        nation = Nation.objects.get(pk=pk)
        if request.user != nation.user:
            return redirect('noEntry')
        else:
            if request.GET.has_key('funds'):  
                if request.GET['funds'] == 'True':
                    error = True
                else:
                    error = False
            else:
                error = False
                
            costs = {'infracost': self.calculate_cost(nation.infrastructure,1), 'techcost': self.calculate_cost(nation.technology,1), 'landcost': self.calculate_cost(nation.land,1)}
            return render_to_response('nations/nation_extend.html',{'form': extendForm(instance=nation), 'nation': Nation.objects.get(pk=pk), 'costs': costs, 'error': error},RequestContext(request))

    def post(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        if request.user != nation.user:
            return redirect('noEntry')
        else:
            data = request.POST

            new_infrastructure = nation.infrastructure + int(data['infrastructure'])
            new_technology = nation.technology + int(data['technology'])
            new_land = nation.land + int(data['land'])

            cost = Decimal(self.calculate_cost(nation.infrastructure,int(data['infrastructure']))) + int(self.calculate_cost(nation.technology,int(data['technology']))) + int(self.calculate_cost(nation.land,int(data['land'])))

            nation.infrastructure = new_infrastructure
            nation.technology = new_technology
            nation.land = new_land
            
            if cost <= nation.funds:
                nation.funds = nation.funds - cost
                nation.save()
                return redirect('/expand/' + pk)
            else:
                return redirect('/expand/' + pk + '?funds=True')

class billsNationView(DetailView):
    model = Nation

    def infrastructure_upkeep(self,infrastructure):
    
        if infrastructure < 100:
            cost = 1
        elif infrastructure >= 100 and infrastructure < 1000:
            cost = 2
        elif infrastructure >= 1000 and infrastructure < 2000:
            cost = 4
        elif infrastructure >= 2000 and infrastructure < 3000:
            cost = 8
        else:
            cost = 15

        return cost

    def calculate_discounts(self, bills, resource1, resource2):
        resources = [resource1,resource2]

        if 'Iron' in resources:
            bills = bills * 0.90
        if 'Lumber' in resources:
            bills = bills * 0.92
        if 'Uranium' in resources:
            bills = bills * 0.97

        return bills

    def get(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        if request.user != nation.user:
            return redirect('noEntry')
        else:
            if request.GET.has_key('funds'):  
                if request.GET['funds'] == 'True':
                    error = True
                else:
                    error = False
            else:
                error = False
            
            costs = {'infrastructure': self.infrastructure_upkeep(nation.infrastructure), 'technology': 2, 'land': 1}
            total_costs = {'infrastructure': self.infrastructure_upkeep(nation.infrastructure)*nation.infrastructure, 'technology': nation.technology*2, 'land': nation.land*1}
            bills = int(nation.infrastructure*self.infrastructure_upkeep(nation.infrastructure)) + int(nation.technology*2) + int(nation.land*1)
            bills = self.calculate_discounts(bills, nation.resource1, nation.resource2)
            
            return render_to_response('nations/nation_bills.html',{'costs': costs, 'nation': nation, 'bills': format(bills,'.2f'), 'total_costs': total_costs, 'new_funds': format(float(nation.funds)-bills,'.2f'), 'error': error},RequestContext(request))

    def post(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        if request.user != nation.user:
            return redirect('noEntry')
        else:
            if Decimal(nation.funds) > Decimal(request.POST['bills']):   
                nation.funds = nation.funds - Decimal(request.POST['bills'])
                nation.save()
                return redirect('/nation/' + pk)
            else:
                return redirect('/bills/' + pk + '?funds=True')

class taxesNationView(DetailView):
    model = Nation
