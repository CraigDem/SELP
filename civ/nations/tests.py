from django.test import Client
from django.test import TestCase
from nations import views
from nations.models import *
import unittest
from nations.views import *

# Create your tests here.

class staticViewTests(TestCase):
	def test_indexView(self):
		c = Client()
		response = c.get('/')
		self.assertEqual(response.status_code, 200)

	def test_noEntry(self):
		c = Client()
		response = c.get('/noEntry/')
		self.assertEqual(response.status_code, 200)

	def rankNationView(self):
		c = Client()
		response = c.get('/rank')
		self.assertEqual(response.status_code, 200)

class registerView(TestCase):
	def test_get(self):
		c = Client()
		response = c.get('/')
		self.assertEqual(response.status_code, 200)

class nationView(TestCase):
	def setUp(self):
		user1 = User.objects.create_user(username='broon', password="")
		user1.set_password('drunkard')
		user1.save()
		nation1 = Nation.objects.create(nation_name='swagland',user=user1,resource1='Aluminium',resource2='Lead',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())
		
		user2 = User.objects.create_user(username='jmac', password="")
		user2.set_password('shortie')
		user2.save()
		nation2 = Nation.objects.create(nation_name='g4sland',user=user2,resource1='Uranium',resource2='Pigs',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())

	def test_anonymous(self):
		# Load the page with a user, should load as normal
		c = Client()
		response = c.get('/nation/1/',follow=True)
		self.assertEqual(response.redirect_chain,[])
		self.assertEqual(response.status_code,200)
		c.logout()

	def test_user(self):
		# Test loading the page with a user
		c = Client()
		c.login(username='broon',password='drunkard')
		response = c.get('/nation/1/',follow=True)
		self.assertEqual(response.redirect_chain,[])
		self.assertEqual(response.status_code,200)
		c.logout()

	# View is open to anyone and doesn't require auth testing.

class editNationView(TestCase):
	def setUp(self):
		# Create two test nations
		user1 = User.objects.create_user(username='broon', password="")
		user1.set_password('drunkard')
		user1.save()
		nation1 = Nation.objects.create(nation_name='swagland',user=user1,resource1='Aluminium',resource2='Lead',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())
		
		user2 = User.objects.create_user(username='jmac', password="")
		user2.set_password('shortie')
		user2.save()
		nation2 = Nation.objects.create(nation_name='g4sland',user=user2,resource1='Uranium',resource2='Pigs',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())

	def test_anonymous(self):
		# Load the page as an anon user, should fail then redirect to a noentry page
		c = Client()
		response = c.get('/edit/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)

	def test_wrong_user(self):
		# Test loading the page with a user that does not belong to the nation, should redirect to no entry
		c = Client()
		c.login(username='jamie',password='shortie')
		response = c.get('/edit/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)
		c.logout()

	def test_right_user(self):
		# Test loading the page with the user that belongs to the nation, should load fine
		c = Client()
		c.login(username='broon',password='drunkard')
		response = c.get('/edit/1/',follow=True)
		self.assertEqual(response.redirect_chain,[])
		self.assertEqual(response.status_code,200)
		c.logout()


class expandNationView(TestCase):
	
	def setUp(self):
		# Create two test nations
		user1 = User.objects.create_user(username='broon', password="")
		user1.set_password('drunkard')
		user1.save()
		nation1 = Nation.objects.create(nation_name='swagland',user=user1,resource1='Aluminium',resource2='Lead',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())
		
		user2 = User.objects.create_user(username='jmac', password="")
		user2.set_password('shortie')
		user2.save()
		nation2 = Nation.objects.create(nation_name='g4sland',user=user2,resource1='Uranium',resource2='Pigs',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())

	def test_anonymous(self):
		# Load the page as an anon user. Should fail and redirect to the noentry page
		c = Client()
		response = c.get('/expand/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)

	def test_wrong_user(self):
		# Test loading the page with a user that does not belong to the nation, should redirect to no entry
		c = Client()
		c.login(username='jmac',password='shortie')
		response = c.get('/expand/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)
		c.logout()

	def test_right_user(self):
		# Test loading the page with the user that belongs to the nation, should load fine
		c = Client()
		c.login(username='broon',password='drunkard')
		response = c.get('/expand/1/',follow=True)
		self.assertEqual(response.redirect_chain,[])
		self.assertEqual(response.status_code,200)
		c.logout()

 	def test_calculate_cost(self):
 		# key values if the if statements
 		c = views.expandNationView()
 		self.assertEqual(c.calculate_cost(99,1),100)
 		self.assertEqual(c.calculate_cost(100,1),200)
 		self.assertEqual(c.calculate_cost(999,2),400)
 		self.assertEqual(c.calculate_cost(1000,2),800)
 		self.assertEqual(c.calculate_cost(1999,2),800)
 		self.assertEqual(c.calculate_cost(2000,1),800)
 		self.assertEqual(c.calculate_cost(2999,1),800)
 		self.assertEqual(c.calculate_cost(3000,1),1000)
 		self.assertEqual(c.calculate_cost(2999,-1),-5)

class billsNationView(TestCase):

	def setUp(self):
		# Create two test nations
		user1 = User.objects.create_user(username='broon', password="")
		user1.set_password('drunkard')
		user1.save()
		nation1 = Nation.objects.create(nation_name='swagland',user=user1,resource1='Aluminium',resource2='Lead',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())
		
		user2 = User.objects.create_user(username='jmac', password="")
		user2.set_password('shortie')
		user2.save()
		nation2 = Nation.objects.create(nation_name='g4sland',user=user2,resource1='Uranium',resource2='Pigs',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())

	def test_anonymous(self):
		# Load the page as an anon user. Should fail and redirect to noentry.
		c = Client()
		response = c.get('/bills/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)

	def test_wrong_user(self):
		# Test loading the page with a user that does not belong to the nation, should redirect to no entry
		c = Client()
		c.login(username='jmac',password='shortie')
		response = c.get('/bills/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)
		c.logout()

	def test_right_user(self):
		# Test loading the page with the user that belongs to the nation, should load fine
		c = Client()
		c.login(username='broon',password='drunkard')
		response = c.get('/bills/1/',follow=True)
		self.assertEqual(response.redirect_chain,[])
		self.assertEqual(response.status_code,200)
		c.logout()

	def test_infrastructure_upkeep(self):
		i = views.billsNationView()

		# Check each boundary of infrastructure upkeep.
		self.assertEqual(i.infrastructure_upkeep(0),1)
 		self.assertEqual(i.infrastructure_upkeep(99),1)
 		self.assertEqual(i.infrastructure_upkeep(100),2)
 		self.assertEqual(i.infrastructure_upkeep(999),2)
 		self.assertEqual(i.infrastructure_upkeep(1000),4)
 		self.assertEqual(i.infrastructure_upkeep(1999),4)
 		self.assertEqual(i.infrastructure_upkeep(2000),8)
 		self.assertEqual(i.infrastructure_upkeep(2999),8)
 		self.assertEqual(i.infrastructure_upkeep(3000),15)

	def test_calculate_discounts(self):
		b = views.billsNationView()
		# Do every combination of resources that have discounts
		self.assertEqual(b.calculate_discounts(100,'Aluminium','Iron'),90)
		self.assertEqual(b.calculate_discounts(100,'Aluminium','Lumber'),92)
		self.assertEqual(b.calculate_discounts(100,'Aluminium','Uranium'),97)
		self.assertEqual(b.calculate_discounts(100,'Iron','Lumber'),82.8)
		self.assertEqual(b.calculate_discounts(100,'Lumber','Uranium'),89.24)
		self.assertEqual(b.calculate_discounts(100,'Iron','Uranium'),87.3)
		
		# And one without discounts just to check
		self.assertEqual(b.calculate_discounts(100,'Aluminium','Lead'),100)

	def test_bills_validation(self): 
		# Create test user
		user1 = User.objects.create_user(username='craig', password="")
		user1.set_password('test')
		user1.save()
		nation1 = Nation.objects.create(nation_name='aplace',user=user1,resource1='Aluminium',resource2='Lead',paid_bills="2014-12-18",collect_taxes=timezone.now().date())
		d = views.billsNationView()

		# If the date given is next year
		self.assertEqual(d.bills_validation(nation1,'2015-12-18'),{'payable': True})
		# Same day as nation last paid bills
		self.assertEqual(d.bills_validation(nation1,'2014-12-18'),{'error': 'Can only pay bills once a day.', 'payable': False})

 	def test_costs_generator(self):
 		# Create test nation	
 		user2 = User.objects.create_user(username='paul', password="")
		user2.set_password('password')
		user2.save()
		nation2 = Nation.objects.create(nation_name='gerland',user=user2,resource1='Aluminium',resource2='Lead',paid_bills="2014-12-18",collect_taxes=timezone.now().date())
 		
 		# Check costs are equal to correct values
 		c = views.billsNationView()
 		self.assertEqual(c.costs_generator(nation2),{'per_technology': 2, 'infrastructure': '1.00', 'new_funds': '9996.00', 'per_infrastructure': 1, 'total': '4.00', 'per_land': 1, 'technology': '2.00', 'land': '1.00'})

class taxesNationView(TestCase):
	def setUp(self):
		# Create two test nations
		user1 = User.objects.create_user(username='broon', password="")
		user1.set_password('drunkard')
		user1.save()
		nation1 = Nation.objects.create(nation_name='swagland',user=user1,resource1='Aluminium',resource2='Lead',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())
		
		user2 = User.objects.create_user(username='jmac', password="")
		user2.set_password('shortie')
		user2.save()
		nation2 = Nation.objects.create(nation_name='g4sland',user=user2,resource1='Uranium',resource2='Pigs',paid_bills=timezone.now().date(),collect_taxes=timezone.now().date())

	def test_anonymous(self):
		# Load page as anon user
		c = Client()
		response = c.get('/taxes/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)

	def test_wrong_user(self):
		# Test loading the page with a user that does not belong to the nation, should redirect to no entry
		c = Client()
		c.login(username='jmac',password='shortie')
		response = c.get('/taxes/1/',follow=True)
		self.assertEqual(response.redirect_chain[0][0],'http://testserver/noEntry/')
		self.assertEqual(response.redirect_chain[0][1],302)
		self.assertEqual(response.status_code,200)
		c.logout()

	def test_right_user(self):
		# Test loading the page with the user that belongs to the nation, should load fine
		c = Client()
		c.login(username='broon',password='drunkard')
		response = c.get('/taxes/1/',follow=True)
		self.assertEqual(response.redirect_chain,[])
		self.assertEqual(response.status_code,200)
		c.logout()

	def test_taxes_validation(self):
		# Create a test nation
		user1 = User.objects.create_user(username='craig', password="")
		user1.set_password('test')
		user1.save()
		nation1 = Nation.objects.create(nation_name='aplace',user=user1,resource1='Aluminium',resource2='Lead',paid_bills="2014-12-18",collect_taxes=timezone.now().date())
		t = views.taxesNationView()

		# If the date given is next year, should be true
		self.assertEqual(t.taxes_validation(nation1,'2015-12-18'),{'payable': True})
		# Same day as nation last paid bills, should be false
		self.assertEqual(t.taxes_validation(nation1,'2014-12-18'),{'error': 'Can only collect taxes once a day.', 'payable': False}) 

	def test_calculate_taxes(self):
		# Create a test nation
		user2 = User.objects.create_user(username='paul', password="")
		user2.set_password('password')
		user2.save()
		nation2 = Nation.objects.create(nation_name='gerland',user=user2,resource1='Aluminium',resource2='Lead',paid_bills="2014-12-18",collect_taxes=timezone.now().date())
		ta = views.taxesNationView()
		# Check the computed taxes for the nation are the same as the correct answer
		self.assertEqual(ta.calculate_taxes(nation2)3000)