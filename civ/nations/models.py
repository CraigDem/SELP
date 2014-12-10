from django.db import models
from django.contrib.auth.models import User

class Nation(models.Model):
    user = models.OneToOneField(User)

    nation_name = models.CharField(max_length=30)
    funds = models.DecimalField(default=10000.00, max_digits=19, decimal_places=2)
    government = models.CharField(max_length=30, default='Democratic')
    religion = models.CharField(max_length=30, default='None')
    infrastructure = models.DecimalField(default=1.00, max_digits=19, decimal_places=2)
    technology = models.DecimalField(default=1.00, max_digits=19, decimal_places=2)
    land = models.DecimalField(default=1.00, max_digits=19, decimal_places=2)
    resource1 = models.CharField(max_length=200)
    resource2 = models.CharField(max_length=200)
    soldiers = models.IntegerField(default=10)
    tanks = models.IntegerField(default=1)
    peaceful = models.BooleanField(default=False)

"""class War(models.Model):
	attacker = models.ForeignKey(UserProfile, related_name='+')
	defender = models.ForeignKey(UserProfile, related_name='+')
	start_date = models.DateField(auto_now_add=True)

class Trade(models.Model):
	initiator = models.ForeignKey(UserProfile, related_name='+')
	reciever = models.ForeignKey(UserProfile, related_name='+')
	start_date = models.DateField(auto_now_add=True)"""


