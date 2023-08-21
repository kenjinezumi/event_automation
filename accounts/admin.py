from django.contrib import admin
from .models import Account, Contact

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'bdr', 'country', 'industry')
    search_fields = ('account_id', 'bdr__name', 'country', 'industry')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'account', 'name', 'seniority', 'email')
    search_fields = ('contact_id', 'account__account_id', 'name', 'email')
