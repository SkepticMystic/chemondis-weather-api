from rest_framework import serializers
from .models import Weather

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = [
          "city",
          "temp_min",
          "temp_max",
          "pressure",
          "humidity",
          "wind_speed",
          "wind_direction",
          "description",
          "timestamp",
        ]
