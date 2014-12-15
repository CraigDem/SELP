from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Nation(models.Model):
    user = models.OneToOneField(User)

    nation_name = models.CharField(max_length=30)
    funds = models.DecimalField(default=10000.00, max_digits=19, decimal_places=2)
    government = models.CharField(max_length=30, default='Democratic')
    religion = models.CharField(max_length=30, default='None')
    infrastructure = models.FloatField(default=1.00)
    technology = models.FloatField(default=1.00)
    land = models.FloatField(default=1.00)
    resource1 = models.CharField(max_length=200)
    resource2 = models.CharField(max_length=200)
    peaceful = models.BooleanField(default=False)
    paid_bills = models.DateField()
    collect_taxes = models.DateField()

"""class War(models.Model):
	attacker = models.ForeignKey(UserProfile, related_name='+')
	defender = models.ForeignKey(UserProfile, related_name='+')
	start_date = models.DateField(auto_now_add=True)

class Trade(models.Model):
	initiator = models.ForeignKey(UserProfile, related_name='+')
	reciever = models.ForeignKey(UserProfile, related_name='+')
	start_date = models.DateField(auto_now_add=True)"""


