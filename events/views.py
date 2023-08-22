from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event
from accounts.models import Contact, Account
import json
import requests
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

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            event = Event.objects.create(
                event_name=data['event_name'],
                registration_page_url=data['registration_page_url'],
                event_date=data['event_date'],
                event_location=data['event_location'],
                maximum_capacity=data['maximum_capacity'],
                target_audience=json.dumps(data['target_audience']),
                event_copy=data['event_copy'],
            )
            print(event)

            if 'contact_lists' in data:
                print('test')
                event.invite_contacts(data['contact_lists'])
                print("End of test")

            return JsonResponse({'id': event.id, 'message': 'Event created successfully' },status=200)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except Contact.DoesNotExist:
            return JsonResponse({'error': 'One or more contacts do not exist'}, status=400)
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



def get_events_for_date(request, year, month, day):
    events = Event.objects.filter(event_date__year=year, event_date__month=month, event_date__day=day)
    event_list = []

    for event in events:
        contacts_attending = Contact.objects.filter(events_attended=event)
        contacts_list = [
            {'contact_name': contact.name, 'contact_seniority': contact.seniority}
            for contact in contacts_attending
        ]

        event_list.append({
            'event_name': event.event_name,
            'event_date': event.event_date,
            'contacts': contacts_list
        })

    return JsonResponse(event_list, safe=False)


@csrf_exempt
def schedule_invite_send(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract data from the request
            contact_id = data['contact_id']
            sender_ldap = data['sender_ldap']
            email_subject = data['email_subject']
            email_body = data['email_body']
            send_datetime = data['send_datetime']

            # Prepare the payload
            payload = {
                'contact_id': contact_id,
                'sender_ldap': sender_ldap,
                'email_subject': email_subject,
                'email_body': email_body,
                'send_datetime': send_datetime
            }

            # Make the POST request to the API URL
            # api_url = 'https://api.eventinvitations.com/v2/cadence_memberships'
            # response = requests.post(api_url, json=payload)
            response.status_code = 200
            if response.status_code == 200:
                return JsonResponse({'message': 'Invite send scheduled successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Failed to schedule invite send'}, status=500)

        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid data: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
