from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event-list'),
    path('events/<int:event_id>/', views.event_detail, name='event-detail'),
    path('events/create/', views.create_event, name='create-event'),
    path('events/update/<int:event_id>/', views.update_event, name='update-event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete-event'),
]
