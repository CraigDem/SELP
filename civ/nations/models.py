from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# This is the model for a nation which definated the types of various attributes of the model. This is converted by django into a database schema.

class Nation(models.Model):
    # Each nation must have a user.
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
    tax_rate = models.IntegerField(default=20)
    citizens = models.IntegerField(default=1)


