from django.db import models


class Account(models.Model):
    bdr = models.ForeignKey('sales.Salesperson', on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    contacts = models.ManyToManyField('Contact', related_name='accounts')
    events_attended = models.ManyToManyField('events.Event', related_name='attending_accounts')


class Contact(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    seniority = models.CharField(max_length=50)
    job_function = models.CharField(max_length=50)
    email = models.EmailField()
    events_attended = models.ManyToManyField('events.Event', related_name='attending_contacts')
    interaction_history = models.TextField()
