from django.db import models


class Account(models.Model):
    account_id = models.CharField(primary_key=True, max_length=50, default='unknown')
    bdr = models.ForeignKey('sales.Salesperson', on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    events_attended = models.ManyToManyField('events.Event', related_name='attending_accounts')

class Contact(models.Model):
    contact_id = models.CharField(primary_key=True, max_length=50, default='unknown')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    seniority = models.CharField(max_length=50)
    job_function = models.CharField(max_length=50)
    email = models.EmailField()
    events_attended = models.ManyToManyField('events.Event', related_name='attending_contacts_ok')
    interaction_history = models.TextField()
