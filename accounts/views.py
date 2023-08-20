from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Contact
import json

# Get list of accounts
def account_list(request):
    accounts = Account.objects.all()
    data = [{'id': account.id, 'country': account.country, 'industry': account.industry} for account in accounts]
    return JsonResponse({'accounts': data})

# Get details of a specific account
def account_detail(request, account_id):
    try:
        account = Account.objects.get(pk=account_id)
        contacts = Contact.objects.filter(account=account)
        contact_data = [{'name': contact.name, 'seniority': contact.seniority, 'job_function': contact.job_function} for contact in contacts]
        data = {
            'id': account.id,
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
                country=data['country'],
                industry=data['industry'],
            )
            return JsonResponse({'id': account.id, 'message': 'Account created successfully'})
        except Salesperson.DoesNotExist:
            return JsonResponse({'error': 'BDR not found'}, status=404)

# Update an account
@csrf_exempt
def update_account(request, account_id):
    try:
        account = Account.objects.get(pk=account_id)
        if request.method == 'PUT':
            data = json.loads(request.body)
            account.country = data['country']
            account.industry = data['industry']
            account.save()
            return JsonResponse({'id': account.id, 'message': 'Account updated successfully'})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

# Delete an account
@csrf_exempt
def delete_account(request, account_id):
    try:
        account = Account.objects.get(pk=account_id)
        account.delete()
        return JsonResponse({'message': 'Account deleted successfully'})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
