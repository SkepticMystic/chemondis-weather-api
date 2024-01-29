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
from django.db.models import Q
from .env import ENV


def refresh_cache(raw_city: str, lang: str) -> Result:
    '''
    Call the open weather api and save the result to the db
    '''

    # call open weather api
    open_weather_result = asyncio.run(get_open_weather(raw_city, lang))
    if (not open_weather_result.ok):
        return open_weather_result

    # save to db
    data = open_weather_result.data

    try:
        weather = Weather(
            lang=lang,
            raw_city=raw_city,
            # NOTE: Don't .lower(), we'll run the query case-insensitively
            resolved_city=data.get("name"),
            country=data.get("sys").get("country"),
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
        return err({
            'status': 500,
            'message': 'Error caching weather',
        })


class WeatherApiView(APIView):
    def get(self, request, city, *args, **kwargs):
        '''
        Get the weather for a given /<str:city>
        Try get a cached result, otherwise call the open weather api
        `lang` query param is optional
        '''

        raw_city = city.lower()
        print('raw_city:', raw_city)
        # TODO: Can this even happen? The route may not match if empty
        if (raw_city == ''):
            return Response(
                err('raw_city param is required').json(),
                status=status.HTTP_400_BAD_REQUEST
            )

        lang = request.query_params.get('lang')
        # SOURCE: https://openweathermap.org/current#multi
        if (
            lang is None or
            lang not in ['en', 'af', 'de']
        ):
            print('unsupported lang:', lang, ', defaulting to en')
            lang = 'en'

        # Try get a cached result
        timestamp__gte = datetime.now(pytz.utc) -\
            timedelta(minutes=ENV.get('CACHE_TTL_MINS'))

        # Implication is that the cache 'key' is city + lang
        # NOTE: We search the cache for raw_ or resolved_city
        #       OpenWeather geocodes multiple inputs to the same output
        weather = Weather.objects\
            .filter(
                (Q(raw_city=raw_city) |
                 Q(resolved_city__iexact=raw_city)) &
                Q(lang=lang) &
                Q(timestamp__gte=timestamp__gte)
            )\
            .last()

        print('cached weather:', weather)

        if (weather is None):
            # Either we don't have a cached result, or it's too old
            refresh_result = refresh_cache(raw_city, lang)

            if (not refresh_result.ok):
                # The err result holds a status code and message
                return Response(
                    err(refresh_result.data.get('message')).json(),
                    status=refresh_result.data.get('status')
                )

            else:
                weather = refresh_result.data

        # Now we have a Weather item to return
        serializer = WeatherSerializer(weather)

        return Response(
            ok(serializer.data).json(),
            status=status.HTTP_200_OK
        )
