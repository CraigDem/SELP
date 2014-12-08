from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    nation_name = models.CharField(max_length=30)
    funds = models.DecimalField(default=10000.00, max_digits=19, decimal_places=2)
    infrastructure = models.IntegerField(default=1)
    technology = models.IntegerField(default=1)
    land = models.IntegerField(default=1)
    resource1 = models.CharField(max_length=200)
    resource2 = models.CharField(max_length=200)


    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

"""class War(models.Model):
	attacker = models.ForeignKey(UserProfile, related_name='+')
	defender = models.ForeignKey(UserProfile, related_name='+')
	start_date = models.DateField(auto_now_add=True)

class Trade(models.Model):
	initiator = models.ForeignKey(UserProfile, related_name='+')
	reciever = models.ForeignKey(UserProfile, related_name='+')
	start_date = models.DateField(auto_now_add=True)"""


