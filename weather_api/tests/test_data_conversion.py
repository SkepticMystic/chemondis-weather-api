from django.test import TestCase
from ..models import Weather
import asyncio
from ..serializers import WeatherSerializer

MOCK_OPEN_WEATHER_RESPONSE = {
    'coord': {
        'lon': -0.1257,
        'lat': 51.5085
    },
    'weather': [{
        'id': 804,
        'main': 'Clouds',
        'description': 'overcast clouds',
        'icon': '04d'
    }],
    'base': 'stations',
    'main': {
        'temp': 281.58,
        'feels_like': 279.43,
        'temp_min': 280.75,
        'temp_max': 282.21,
        'pressure': 1031,
        'humidity': 76
    },
    'visibility': 10000,
    'wind': {
        'speed': 3.6,
        'deg': 200
    },
    'clouds': {
        'all': 100
    },
    'dt': 1706368118,
    'sys': {
        'type': 2,
        'id': 2075535,
        'country': 'GB',
        'sunrise': 1706341618,
        'sunset': 1706373541
    },
    'timezone': 0,
    'id': 2643743,
    'name': 'London',
    'cod': 200
}


class TestDataConversion(TestCase):

    # Check that a well-formed request is successful
    def test_happy_path(self):
        raw_city = 'london'
        lang = 'en'

        weather = Weather.open_weather_to_model(
            raw_city, lang, MOCK_OPEN_WEATHER_RESPONSE)

        self.assertEqual(weather.raw_city, raw_city)
        self.assertEqual(weather.resolved_city, 'London')
        self.assertEqual(weather.country, 'GB')
        self.assertEqual(weather.description, 'overcast clouds')
        self.assertEqual(weather.temp, 281.58)
        self.assertEqual(weather.temp_min, 280.75)
        self.assertEqual(weather.temp_max, 282.21)
        self.assertEqual(weather.pressure, 1031)
        self.assertEqual(weather.humidity, 76)
        self.assertEqual(weather.wind_speed, 3.6)
        self.assertEqual(weather.wind_direction, 'south')
        self.assertEqual(weather.lang, lang)

    # Check that an invalid input raises an exception
    def test_invalid_input(self):
        raw_city = 'london'
        lang = 'en'

        with self.assertRaises(Exception):
            Weather.open_weather_to_model(
                raw_city, lang, {'invalid': 'response'})
