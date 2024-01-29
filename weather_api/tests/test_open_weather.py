from django.test import TestCase
from ..open_weather import get_open_weather
import asyncio


class TestOpenWeather(TestCase):

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_happy_path(self):
        result = asyncio.run(get_open_weather('london', 'en'))

        # The get_open_weather function checks response.cod == 200
        # So checking for result.ok is equivalent
        self.assertTrue(result.ok, result)

    # NOTE: We check for 'city not found' in test_requests.py
    # But just to be sure, we check for it here too
    def test_city_not_found(self):
        result = asyncio.run(get_open_weather('mumb', 'en'))

        self.assertFalse(result.ok, result)
        self.assertEqual(
            result.data.get('message'),
            'city not found',
            result
        )
