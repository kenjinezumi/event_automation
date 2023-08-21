from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from .models import Account, Contact

from sales.models import Salesperson
import json

# Get list of accounts
def account_list(request):
    accounts = Account.objects.values('account_id').annotate(count=Count('account_id'))
    unique_account_id = [entry['account_id'] for entry in accounts if entry['count'] > 0]
    return JsonResponse({'account_id': unique_account_id})

def country_list(request):
    countries = Account.objects.values('country').annotate(count=Count('country'))
    unique_country = [entry['country'] for entry in countries if entry['count'] > 0]
    return JsonResponse({'country': unique_country})

def industries_list(request):
    accounts = Account.objects.values('industry').annotate(count=Count('industry'))
    unique_industries = [entry['industry'] for entry in accounts if entry['count'] > 0]
    return JsonResponse({'industries': unique_industries})

def functions_list(request):
    accounts = Contact.objects.values('job_function').annotate(count=Count('job_function'))
    unique_functions = [entry['job_function'] for entry in accounts if entry['count'] > 0]
    return JsonResponse({'job_function': unique_functions})

def seniority_list(request):
    accounts = Contact.objects.values('seniority').annotate(count=Count('seniority'))
    unique_seniority = [entry['seniority'] for entry in accounts if entry['count'] > 0]
    return JsonResponse({'seniority': unique_seniority})

# Get details of a specific account
def account_detail(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
        contacts = Contact.objects.filter(account=account)
        contact_data = [{'name': contact.name, 'seniority': contact.seniority, 'job_function': contact.job_function} for contact in contacts]
        data = {
            'account_id': account.account_id,
            'bdr': account.bdr.name,
            'country': account.country,
            'industry': account.industry,
            'contacts': contact_data,
        }
        return JsonResponse(data)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

# Create a new account
@csrf_exempt
def create_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bdr_id = data['bdr_id']
        try:
            bdr = Salesperson.objects.get(pk=bdr_id)
            account = Account.objects.create(
                bdr=bdr,
                account_id=data['account_id'],
                country=data['country'],
                industry=data['industry'],
            )
            return JsonResponse({'account_id': account.account_id, 'message': 'Account created successfully'})
        except Salesperson.DoesNotExist:
            return JsonResponse({'error': 'BDR not found'}, status=404)

# Update an account
@csrf_exempt
def update_account(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
        if request.method == 'PUT':
            data = json.loads(request.body)
            account.country = data['country']
            account.industry = data['industry']
            account.save()
            return JsonResponse({'account_id': account.account_id, 'message': 'Account updated successfully'})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

# Delete an account
@csrf_exempt
def delete_account(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
        account.delete()
        return JsonResponse({'message': 'Account deleted successfully'})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
