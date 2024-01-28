from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Weather
from .serializers import WeatherSerializer
from datetime import datetime, timedelta
import pytz
from .open_weather import get_open_weather
from .result import ok, err, Result
import asyncio
from .env import ENV


def refresh_cache(city: str, lang: str) -> Result:
    '''
    Call the open weather api and save the result to the db
    '''

    # call open weather api
    open_weather_result = asyncio.run(get_open_weather(city, lang))
    if (not open_weather_result.ok):
        return open_weather_result

    # save to db
    data = open_weather_result.data

    try:
        weather = Weather(
            city=city,
            lang=lang,
            temp=data.get("main").get("temp"),
            temp_min=data.get("main").get("temp_min"),
            temp_max=data.get("main").get("temp_max"),
            pressure=data.get("main").get("pressure"),
            humidity=data.get("main").get("humidity"),
            wind_speed=data.get("wind").get("speed"),
            # TODO: Convert this to north, south, east, west
            wind_direction=data.get("wind").get("deg"),
            description=data.get("weather")[0].get("description"),
        )

        weather.save()

        return ok(weather)

    except Exception as e:
        print('refresh_cache exception:', e)
        return err(e)


class WeatherApiView(APIView):
    def get(self, request, city, *args, **kwargs):
        '''
        Get the weather for a given /<str:city>
        Try get a cached result, otherwise call the open weather api
        `lang` query param is optional
        '''

        print('city:', city)
        if (city == ''):
            return Response(
                err('city param is required').json(),
                status=status.HTTP_400_BAD_REQUEST
            )

        # standardize city input
        city = city.lower()

        lang = request.query_params.get('lang')
        # SOURCE: https://openweathermap.org/current#multi
        if (lang is None or (lang not in ['af', 'de'])):
            print('unsupported lang:', lang, ', defaulting to en')
            lang = 'en'

        # Try get a cached result
        timestamp__gte = datetime.now(pytz.utc) -\
            timedelta(minutes=ENV.get('CACHE_TTL_MINS'))

        # Implication is that the cache 'key' is city + lang
        weather = Weather.objects\
            .filter(
                city=city,
                lang=lang,
                timestamp__gte=timestamp__gte
            )\
            .last()

        print('cached weather:', weather)

        if (weather is None):
            # Either we don't have a cached result, or it's too old
            refresh_result = refresh_cache(city, lang)

            if (not refresh_result.ok):
                return Response(
                    refresh_result.json(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            else:
                weather = refresh_result.data

        # Now we have a Weather item to return
        serializer = WeatherSerializer(weather)

        return Response(
            ok(serializer.data).json(),
            status=status.HTTP_200_OK
        )
