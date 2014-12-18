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

# rankNationView handles the logic and generation of the nation registration pages
class registerView(View):
	
	registered = False

	def get(self, request):
		# Get the user creation form and then pass it to the user
		user_form = UserForm()
		return render_to_response('registration/register.html',{'user_form': user_form, 'registered': self.registered}, RequestContext(request))

	def post(self, request):
		# Get the data inputted by the user
		user_form = UserForm(data=request.POST)

		# List of possible resources for a nation to have. Two random non-identical resouces will be chosen from this list.
		resources = random.sample(set(['Aluminium','Cattle','Coal','Fish','Furs','Gold','Gems','Iron','Lead','Lumber','Marble','Oil','Pigs','Rubber','Silver','Spices','Sugar','Uranium','Water','Wheat','Wine']),2)
		
		# If the inputted data from the user is valid 
		if user_form.is_valid():

			# Create a user object, assign it the appropriate password then save the object.
			user = User.objects.create_user(username=user_form['username'].value(), password='')
			user.set_password(user_form['password'].value())
			user.save()
			# When the user account is being created, create a nation at the same time.
			Nation.objects.create(nation_name=user_form['nation_name'].value(),user=user,resource1=resources[0],resource2=resources[1],paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())

			# Set registered to true, this will be passed to the template 
			registered = True

		# If the inputted data from the user is invalid, set registered to false and print the error into the terminal.
		else:
			registered = False
			print user_form.errors
		# Render the page with approprate form and registration status.
		return render_to_response('registration/register.html',{'user_form': user_form, 'registered': registered},RequestContext(request))

# nationView simply displays information about a given nation
class nationView(DetailView):
	model = Nation

# editNationView handles the logic and generation of editing the nation 
class editNationView(UpdateView, ModelFormMixin):
	# The model to be editted is a nation, using the NationForm form
	model = Nation
	form_class = NationForm

	def get(self, request, pk):
		# Get the nation object to edit
		nation = Nation.objects.get(pk=pk)

		# If not their own nation, redirect to error page
		if request.user != nation.user:
			return redirect('noEntry')
		else:   
			# Pass the form and nation to the template
			return render_to_response('nations/nation_form.html',{'form': NationForm(instance=nation), 'nation': nation},RequestContext(request))

	def post(self, request, pk):
		# Get the nation object to edit
		nation = Nation.objects.get(pk=pk)

		# If not their own nation, redirect to error page
		if request.user != nation.user:
			# If not their own nation, redirect to error page
			return redirect('noEntry')
		else:
			# Get the inpputed date then check it is valid. Is it is then save the new nation and redirect to display the nation.
			nation_form = NationForm(data=request.POST, instance=nation)
			if nation_form.is_valid():
				nation_form.save()
				return redirect('/nation/' + pk)
			# Pass any form errors and the nation to the form
			return render_to_response('nations/nation_form.html',{'form_errors': nation_form.errors, 'nation':nation},RequestContext(request))

# expandNationView handles the logic and generation of the purchasing and selling parts of the nation
class expandNationView(UpdateView, ModelFormMixin):

	model = Nation
	form_class = extendForm

	def get(self, request, pk):
		# Get the nation object to edit
		nation = Nation.objects.get(pk=pk)

		# If not their own nation, redirect to error page
		if request.user != nation.user:
			return redirect('noEntry')
		else:
			# If there is a funds flag then set the error variable to true, otherwise false
			if request.GET.has_key('funds'):  
				if request.GET['funds'] == 'True':
					error = True
				else:
					error = False
			else:
				error = False
			# Create a dictionary containing the costs of each unit of infrastructure, technology and land. 
			costs = {'infracost': self.calculate_cost(nation.infrastructure,1), 'techcost': self.calculate_cost(nation.technology,1), 'landcost': self.calculate_cost(nation.land,1)}
			return render_to_response('nations/nation_extend.html',{'form': extendForm(instance=nation), 'nation': Nation.objects.get(pk=pk), 'costs': costs, 'error': error},RequestContext(request))

	def post(self, request, pk):
		# Get the nation object to edit
		nation = Nation.objects.get(pk=pk)
		# If not their own nation, redirect to error page
		if request.user != nation.user:
			return redirect('noEntry')
		else:
			# Get the inputted data, calculate the new infrastructure, technology and land levels.
			data = request.POST

			new_infrastructure = nation.infrastructure + int(data['infrastructure'])
			new_technology = nation.technology + int(data['technology'])
			new_land = nation.land + int(data['land'])

			# Calculate the cost by adding together the amount of infrastructure multipled by the cost, doing the same for technology and land then adding the three totals together
			cost = Decimal(self.calculate_cost(nation.infrastructure,int(data['infrastructure']))) + int(self.calculate_cost(nation.technology,int(data['technology']))) + int(self.calculate_cost(nation.land,int(data['land'])))
 
			# If the nation has enough funds to fund their purchases, set the nation's attributes to their new levels then save the nation. Otherwise, display the expansion page again but with the funds attribute passed via a GET request.
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
	# This function will take in the current level of a nation's attribute, as well as the amount of an attribute to be bought and will output the cost          
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
				
# billsNationView handles the logic and generation of the page to pay bills
class billsNationView(DetailView):
	model = Nation
	
	def get(self, request, pk):
		# Get the nation object to edit
		nation = Nation.objects.get(pk=pk)
		
		if request.user != nation.user:
			return redirect('noEntry')
		else:        
			return render_to_response('nations/nation_bills.html',{'costs': self.costs_generator(nation), 'nation': nation, 'validate': self.bills_validation(nation, datetime.datetime.now().date())},RequestContext(request))

	def post(self, request, pk):
		# Get the nation object to edit
		nation = Nation.objects.get(pk=pk)

		# If not the user's own nation, redirect to error page
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

	# This function will take in a level of infrastructure and output the cost per unit of infratructure
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

	# This function will take in the cost of bills or a nation, along with the nation's resources and then will check to see if there are any applicable discounts to the bills.
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
	  
	# This function checks to see if the nation can pay it's bills and will return an appropriate error if it cannot.
	def bills_validation(self, nation, date): 
		# check to see if the nation has already paid it's bills on a given day.
		if nation.paid_bills == date:
			return {'payable': False, 'error': 'Can only pay bills once a day.'}
		else:
			# Calculate the bills for infrastructure, then all bills together.
			infrastructure = self.calculate_discounts(self.infrastructure_upkeep(nation.infrastructure)*nation.infrastructure,nation.resource1,nation.resource2)
			total_bills = infrastructure+nation.technology*2+nation.land*1
			
			# If the nation has the funds to pay its bills, return true, otherwsie return false and a related error.
			if nation.funds > total_bills:
				return {'payable': True}
			else:
				return {'payable': False, 'error': 'Not enough funds'}  		
	
	# This function will take in a nation and return a dictionary specifing that nation's bills both per unit and overall, as well as the funds after bills being hypothetically paid.
	def costs_generator(self, nation):
		infrastructure = self.calculate_discounts(self.infrastructure_upkeep(nation.infrastructure)*nation.infrastructure,nation.resource1,nation.resource2)
		total_bills = infrastructure+nation.technology*2+nation.land*1
		new_funds = float(nation.funds) - total_bills
		return {'per_infrastructure': self.infrastructure_upkeep(nation.infrastructure), 'per_technology': 2, 'per_land': 1, 'infrastructure': format(infrastructure,'.2f'), 'technology': format(nation.technology*2,'.2f'), 'land': format(nation.land*1,'.2f'), 'total': format(total_bills,'.2f'), 'new_funds': format(new_funds,'.2f')}

# taxesNationView handles the logic and generation of the page to collect taxes.
class taxesNationView(DetailView):
	model = Nation

	def get(self, request, pk):
		# Get the nation object to edit.
		nation = Nation.objects.get(pk=pk)
		
		# If not the user's own nation, redirect to error page
		if request.user != nation.user:
			return redirect('noEntry')
		else:        
			# calculate what the new funds would be after collecting taxes and pass the information to the template
			new_funds = nation.funds + Decimal(self.calculate_taxes(nation))
			return render_to_response('nations/nation_taxes.html',{'taxes': format(self.calculate_taxes(nation),'.2f'), 'new_funds': format(new_funds,'.2f'), 'nation': nation, 'validate': self.taxes_validation(nation, datetime.datetime.now().date())},RequestContext(request))

	def post(self, request, pk):
		# Get the nation object to edit.
		nation = Nation.objects.get(pk=pk)

		 # If not the user's own nation, redirect to error page
		if request.user != nation.user:
			return redirect('noEntry')
		else:
			# Check the nation can collect its' taxes, and if it can then set the nation's attributes appropriately then save changes. Otherwise just load the taxes page again.
			if self.taxes_validation(nation,datetime.datetime.now().date()):
				nation.funds = nation.funds + Decimal(request.POST['taxes'])
				nation.collect_taxes = datetime.datetime.now().date()
				nation.save()
				return redirect('/nation/' + pk)
			else:
				return redirect('/taxes/' + pk)
	
	# This function checks to see if a nation can collect its' taxes and will return a related error if it can't.
	def taxes_validation(self, nation, date): 
		# Check taxes not have already been collected on a given day, otherwise return true.
		if nation.collect_taxes == date:
			return {'payable': False, 'error': 'Can only collect taxes once a day.'}
		else:
			return {'payable': True}
	
	# This function calculates how many taxes a nation has to collect
	def calculate_taxes(self,nation):
		return nation.citizens * (15000*(float(nation.tax_rate)/100))
	
# rankNationView handles the logic and generation of the ranking nations page.
class rankNationView(DetailView):
	def get(self,request):
		# This dictionary contains the rank 1 of each category.
		rank1 = {'infrastructure': Nation.objects.order_by('infrastructure').reverse()[0], 'technology': Nation.objects.order_by('technology').reverse()[0], 'land': Nation.objects.order_by('land').reverse()[0]}
		# Return the top 100 nations. This is assumed to be by infrastructure but this is not a completely accurate way to get top 100.
		nations = Nation.objects.order_by('infrastructure')[0:100]
		print len(nations)
		nation_count = range(1,len(nations)+1)

		# Pass these pieces of information to the template
		return render_to_response('nations/nation_rank.html',{'nations': nations, 'nation_count': nation_count, 'rank1': rank1},RequestContext(request))