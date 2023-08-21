from django.contrib import admin
from .models import Salesperson, Lead, Opportunity


@admin.register(Salesperson)
class SalespersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'assigned_salesperson')
    list_filter = ('assigned_salesperson',)
    search_fields = ('name', 'email')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('lead', 'event', 'status', 'value')
    list_filter = ('lead', 'event', 'status')
    search_fields = ('lead__name', 'event__event_name')
