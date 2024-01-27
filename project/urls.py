from django.contrib import admin
from django.urls import path, include
from weather_api import urls as weather_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('weather/', include(weather_urls)),
]
