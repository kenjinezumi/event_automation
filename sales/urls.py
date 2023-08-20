from django.urls import path
from . import views

urlpatterns = [
    path('salespeople/', views.salesperson_list, name='salesperson-list'),
    path('salespeople/<int:salesperson_id>/', views.salesperson_detail, name='salesperson-detail'),
    path('salespeople/create/', views.create_salesperson, name='create-salesperson'),
    path('salespeople/update/<int:salesperson_id>/', views.update_salesperson, name='update-salesperson'),
    path('salespeople/delete/<int:salesperson_id>/', views.delete_salesperson, name='delete-salesperson'),
]
