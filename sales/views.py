from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Salesperson, Lead, Opportunity
import json

# Get list of salespeople
def salesperson_list(request):
    salespeople = Salesperson.objects.all()
    data = [{'id': salesperson.id, 'name': salesperson.name, 'email': salesperson.email} for salesperson in salespeople]
    return JsonResponse({'salespeople': data})

# Get details of a specific salesperson
def salesperson_detail(request, salesperson_id):
    try:
        salesperson = Salesperson.objects.get(pk=salesperson_id)
        leads = Lead.objects.filter(assigned_salesperson=salesperson)
        lead_data = [{'name': lead.name, 'email': lead.email} for lead in leads]
        data = {
            'id': salesperson.id,
            'name': salesperson.name,
            'email': salesperson.email,
            'leads': lead_data,
        }
        return JsonResponse(data)
    except Salesperson.DoesNotExist:
        return JsonResponse({'error': 'Salesperson not found'}, status=404)

# Create a new salesperson
@csrf_exempt
def create_salesperson(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        salesperson = Salesperson.objects.create(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
        )
        return JsonResponse({'id': salesperson.id, 'message': 'Salesperson created successfully'})

# Update a salesperson
@csrf_exempt
def update_salesperson(request, salesperson_id):
    try:
        salesperson = Salesperson.objects.get(pk=salesperson_id)
        if request.method == 'PUT':
            data = json.loads(request.body)
            salesperson.name = data['name']
            salesperson.email = data['email']
            salesperson.phone_number = data['phone_number']
            salesperson.save()
            return JsonResponse({'id': salesperson.id, 'message': 'Salesperson updated successfully'})
    except Salesperson.DoesNotExist:
        return JsonResponse({'error': 'Salesperson not found'}, status=404)

# Delete a salesperson
@csrf_exempt
def delete_salesperson(request, salesperson_id):
    try:
        salesperson = Salesperson.objects.get(pk=salesperson_id)
        salesperson.delete()
        return JsonResponse({'message': 'Salesperson deleted successfully'})
    except Salesperson.DoesNotExist:
        return JsonResponse({'error': 'Salesperson not found'}, status=404)
