# Import Statements - Django

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic import View, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.forms.models import BaseModelFormSet
from nations.forms import UserForm, NationForm, extendForm
from nations.models import Nation

# Import Statements - Python

from decimal import Decimal
import datetime
import random

"""

This application uses a class based view structure. Each view is materialised as a Python class, with helper functions:

get(self,request): This function will run in the event a given class is activated with a HTTP GET request.

post(self,request): This function will run in the event a given class is activated with a HTTP POST request.

Any functions other than the get or post functions in a class will be functions required to calculate results pertaining to their respective class view.

"""

# indexView generates the homepage, "/"
class indexView(View):

    def get(self, request):
	    # Render the home page's template
    	return render(request,'nations/home.html',{})

# indexView generates the error page regarding not having permission to rule anothers' nation, "/no_entry"
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
 
            if cost <= nation.funds:
            	nation.infrastructure = new_infrastructure
            	nation.technology = new_technology
            	nation.land = new_land
            	nation.citizens = int(new_infrastructure*5+new_land*2)
                nation.funds = nation.funds - cost
                nation.save()
                return redirect('/expand/' + pk)
            else:
                return redirect('/expand/' + pk + '?funds=True')
                
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
                
	
class billsNationView(DetailView):
    model = Nation
    
    def get(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        
        if request.user != nation.user:
            return redirect('noEntry')
        else:        
            return render_to_response('nations/nation_bills.html',{'costs': self.costs_generator(nation), 'nation': nation, 'validate': self.bills_payable(nation, datetime.datetime.now().date())},RequestContext(request))

    def post(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        if request.user != nation.user:
            return redirect('noEntry')
        else:
            if self.bills_validation(nation,datetime.datetime.now().date()):
            	nation.funds = nation.funds - Decimal(request.POST['bills'])
            	nation.paid_bills = datetime.datetime.now().date()
            	nation.save()
            	return redirect('/nation/' + pk)
            else:
            	return redirect('/bills/' + pk)

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
        bills = float(bills)
        if 'Iron' in resources:
            bills = bills * 0.90
        if 'Lumber' in resources:
            bills = bills * 0.92
        if 'Uranium' in resources:
            bills = bills * 0.97

        return bills
        
    def bills_validation(self, nation, date): 
	    if nation.paid_bills == date:
	    	return {'payable': False, 'error': 'Can only pay bills once a day.'}
	    else:
	    	infrastructure = self.calculate_discounts(self.infrastructure_upkeep(nation.infrastructure)*nation.infrastructure,nation.resource1,nation.resource2)
	    	total_bills = infrastructure+nation.technology*2+nation.land*1
	    	
	    	if nation.funds > total_bills:
	    		return {'payable': True}
	    	else:
	    		return {'payable': False, 'error': 'Not enough funds'}  		
	
    def costs_generator(self, nation):
	    infrastructure = self.calculate_discounts(self.infrastructure_upkeep(nation.infrastructure)*nation.infrastructure,nation.resource1,nation.resource2)
	    total_bills = infrastructure+nation.technology*2+nation.land*1
	    new_funds = float(nation.funds) - total_bills
	    return {'per_infrastructure': self.infrastructure_upkeep(nation.infrastructure), 'per_technology': 2, 'per_land': 1, 'infrastructure': format(infrastructure,'.2f'), 'technology': format(nation.technology*2,'.2f'), 'land': format(nation.land*1,'.2f'), 'total': format(total_bills,'.2f'), 'new_funds': format(new_funds,'.2f')}

class taxesNationView(DetailView):
    model = Nation
    
    def get(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        
        if request.user != nation.user:
            return redirect('noEntry')
        else:        
        	new_funds = nation.funds + Decimal(self.calculate_taxes(nation))
        	return render_to_response('nations/nation_taxes.html',{'taxes': format(self.calculate_taxes(nation),'.2f'), 'new_funds': format(new_funds,'.2f'), 'nation': nation, 'validate': self.taxes_validation(nation, datetime.datetime.now().date())},RequestContext(request))

    def post(self, request, pk):
        nation = Nation.objects.get(pk=pk)
        if request.user != nation.user:
            return redirect('noEntry')
        else:
            if self.taxes_validation(nation,datetime.datetime.now().date()):
            	nation.funds = nation.funds + Decimal(request.POST['taxes'])
            	nation.collect_taxes = datetime.datetime.now().date()
            	nation.save()
            	return redirect('/nation/' + pk)
            else:
            	return redirect('/taxes/' + pk)
    
    def taxes_validation(self, nation, date): 
	    if nation.collect_taxes == date:
	    	return {'payable': False, 'error': 'Can only collect taxes once a day.'}
	    else:
	    	return {'payable': True}
    
    def calculate_taxes(self,nation):
	    return nation.citizens * (15000*(float(nation.tax_rate)/100))
    
# rankNationView handles the logic and generation of the ranking nations page.
class rankNationView(View):
	def get(self,request):
		rank1 = {'infrastructure': Nation.objects.order_by('infrastructure').reverse()[0], 'technology': Nation.objects.order_by('technology').reverse()[0], 'land': Nation.objects.order_by('land').reverse()[0]}
		nations = Nation.objects.order_by('infrastructure')[0:100]
		return render_to_response('nations/nation_rank.html',{'nations': nations, 'rank1': rank1},{})