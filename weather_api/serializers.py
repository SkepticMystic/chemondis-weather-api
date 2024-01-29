from rest_framework import serializers
from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='resolved_city')

    class Meta:
        model = Weather
        fields = [
            "city",
            "country",
            "temp",
            "temp_min",
            "temp_max",
            "pressure",
            "humidity",
            "wind_speed",
            "wind_direction",
            "description",
            "timestamp",
        ]
