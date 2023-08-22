from django.db import models
from accounts.models import Contact  # Import the Contact model from your app

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    registration_page_url = models.URLField()
    event_date = models.DateTimeField()
    event_location = models.CharField(max_length=100)
    maximum_capacity = models.PositiveIntegerField()
    target_audience = models.TextField()  # TODO Store JSON data here
    event_copy = models.TextField()

    def invite_contacts(self, contact_emails):
        """
        Invite contacts to the event by creating Invitation objects.
        """
        invitations = []
        print(contact_emails)
        for contact_id in contact_emails:
            contact = Contact.objects.get(contact_id=contact_id)
            invitation = Invitation(event=self, contact=contact)
            invitations.append(invitation)
        Invitation.objects.bulk_create(invitations)

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='invitations')
    sent_datetime = models.DateTimeField(auto_now_add=True)  # Use auto_now_add to set the sent_datetime automatically
