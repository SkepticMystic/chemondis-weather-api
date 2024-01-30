from django.contrib import admin
from django.urls import path, include
from weather_api import urls as weather_urls
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('weather/<str:city>', include(weather_urls)),
]
