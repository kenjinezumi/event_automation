from django.db import models
from accounts.models import Account  # Import the Account model from your app
from events.models import Event  # Import the Event model from the events app

class Salesperson(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    assigned_accounts = models.ManyToManyField(Account, related_name='assigned_salespeople')

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    assigned_salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    interaction_history = models.TextField()

class Opportunity(models.Model):
    lead = models.ForeignKey('sales.Lead', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=10, decimal_places=2)