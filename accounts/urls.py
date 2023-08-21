from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
)

urlpatterns = [
    path('accounts/', views.account_list, name='account-list'),
    path('industries/', views.industries_list, name='industries-list'),
    path('functions/', views.functions_list, name='functions-list'),
    path('seniority/', views.seniority_list, name='seniority-list'),
    path('countries/', views.country_list, name='country-list'),

    path('accounts/<int:account_id>/', views.account_detail, name='account-detail'),
    path('accounts/create/', views.create_account, name='create-account'),
    path('accounts/update/<int:account_id>/', views.update_account, name='update-account'),
    path('accounts/delete/<int:account_id>/', views.delete_account, name='delete-account'),
]
