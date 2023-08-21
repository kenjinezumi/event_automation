from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event
import json

# Get list of events
def event_list(request):
    events = Event.objects.all()
    data = [{'id': event.id, 'event_name': event.event_name, 'event_date': event.event_date} for event in events]
    return JsonResponse({'events': data})

# Get details of a specific event
def event_detail(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        data = {
            'id': event.id,
            'event_name': event.event_name,
            'event_date': event.event_date,
            'event_location': event.event_location,
            'maximum_capacity': event.maximum_capacity,
            'target_audience': json.loads(event.target_audience),
            'event_copy': event.event_copy,
        }
        return JsonResponse(data)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

# Create a new event
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = Event.objects.create(
                event_id=data['event_id'],
                event_name=data['event_name'],
                registration_page_url=data['registration_page_url'],
                event_date=data['event_date'],
                event_location=data['event_location'],
                maximum_capacity=data['maximum_capacity'],
                target_audience=json.dumps(data['target_audience']),
                event_copy=data['event_copy'],
            )
            return JsonResponse({'id': event.id, 'message': 'Event created successfully'})
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid data: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
# Update an event
@csrf_exempt
def update_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        if request.method == 'PUT':
            data = json.loads(request.body)
            event.event_name = data['event_name']
            event.registration_page_url = data['registration_page_url']
            event.event_date = data['event_date']
            event.event_location = data['event_location']
            event.maximum_capacity = data['maximum_capacity']
            event.target_audience = json.dumps(data['target_audience'])
            event.event_copy = data['event_copy']
            event.save()
            return JsonResponse({'id': event.id, 'message': 'Event updated successfully'})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

# Delete an event
@csrf_exempt
def delete_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully'})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
