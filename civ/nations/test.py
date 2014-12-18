from django.test import Client
from django.test import TestCase
from nations import views
import unittest

# Create your tests here.

class simpleTests(unittest.TestCase):
	def indexView(self):
		response = self.client.get('/')
		assertEqual(response.status_code, 200)

	def noEntry(self):
		response = self.client.get('/no_entry')
		assertEqual(response.status_code, 200)

# class noEntry(View):

# class registerView(View):

# class nationView(DetailView):

class editNationView(unittest.TestCase):
	def anonymous(self):
		response = self.client.get('nation/1',follow=True)
		print "test" + str(response.redirect_chain)
		#assertEqual(response.chain[:1])


# class expandNationView(UpdateView, ModelFormMixin):

# 	def calculate_cost(self,level,amount):

# class billsNationView(DetailView):

# 	def infrastructure_upkeep(self,infrastructure):

#	def calculate_discounts(self, bills, resource1, resource2):

#	def bills_validation(self, nation, date): 

# 	def costs_generator(self, nation):

# class taxesNationView(DetailView):

#	def taxes_validation(self, nation, date): 

#	def calculate_taxes(self,nation):

# class rankNationView(DetailView):

if __name__ == '__main__':
	unittest.main()