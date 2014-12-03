from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Nation(models.Model):
	ruler = models.ForeignKey(User)
	infrastructure = models.IntegerField(default=1)
	technology = models.IntegerField(default=1)
	land = models.IntegerField(default=1)
	resource_1 = models.CharField(max_length=200)
	resource_2 = models.CharField(max_length=200)

class War(models.Model):
	attacker = models.ForeignKey(Nation, related_name='+')
	defender = models.ForeignKey(Nation, related_name='+')
	start_date = models.DateField(auto_now_add=True)

class Trade(models.Model):
	initiator = models.ForeignKey(Nation, related_name='+')
	reciever = models.ForeignKey(Nation, related_name='+')
	start_date = models.DateField(auto_now_add=True)


