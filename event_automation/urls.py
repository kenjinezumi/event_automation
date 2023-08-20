"""event_automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse
from django.urls import URLPattern, URLResolver
import re
from django.conf import settings

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


def list_apis(urlpatterns, parent_pattern=''):
    api_list = []

    for url_pattern in urlpatterns:
        if isinstance(url_pattern, URLPattern):
            api_list.append(parent_pattern + str(url_pattern.pattern))
        elif isinstance(url_pattern, URLResolver):
            api_list.extend(list_apis(url_pattern.url_patterns, parent_pattern + str(url_pattern.pattern)))

    return api_list


def api_list(request):
    urlpatterns = __import__(settings.ROOT_URLCONF, fromlist=['urlpatterns']).urlpatterns
    apis = list_apis(urlpatterns)
    return JsonResponse({'apis': apis})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('events.urls')),  # Include 'events' app URLs
    path('api/', include('sales.urls')),  # Include 'sales' app URLs
    path('api/', include('accounts.urls')),  # Include 'accounts' app URLs
    path('api-list/', api_list, name='api-list'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

