from django.urls import re_path, include
from .views import (
    WeatherApiView,
)

urlpatterns = [
    re_path('api', WeatherApiView.as_view()),
]