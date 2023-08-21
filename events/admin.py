from django.contrib import admin
from .models import Event, Invitation

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'event_location', 'maximum_capacity')
    search_fields = ('event_name', 'event_location')

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('event', 'contact', 'sent_datetime')
    list_filter = ('event', 'contact')
    search_fields = ('event__event_name', 'contact__name')
