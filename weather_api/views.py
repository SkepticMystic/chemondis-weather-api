from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeatherSerializer
from .result import ok, err
from .env import ENV
from .cache import WeatherCache

SUPPORTED_LANGS = ['en', 'af', 'de']
CACHE_TTL_MINS = ENV.get('CACHE_TTL_MINS')


class WeatherApiView(APIView):
    def get(self, request, city, *args, **kwargs):
        '''
        Get the weather for a given /<str:city>
        Try get a cached result, otherwise call the Open Weather api
        `lang` query param optionally specifies the language
        '''

        # NOTE: raw_city can't be None or '', otherwise the route wouldn't match.
        #       So we can assume it's a non-empty string
        raw_city = city.lower()

        # See source for other supported languages: https://openweathermap.org/current#multi
        lang = request.query_params.get('lang')
        if (lang is None):
            lang = SUPPORTED_LANGS[0]
        elif (lang not in SUPPORTED_LANGS):
            return Response(
                err(f'Unsupported language. Valid inputs: {SUPPORTED_LANGS}')
                .json(),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try get a cached result
        weather_result = WeatherCache.get_weather(raw_city, lang)

        if (not weather_result.ok):
            # The err result holds a status code and message
            return Response(
                err(weather_result.data.get('message')).json(),
                status=weather_result.data.get('status')
            )

        # Now we have a Weather item to return
        serializer = WeatherSerializer(weather_result.data.get('weather'))

        return Response(
            ok(serializer.data).json(),
            status=status.HTTP_200_OK,
            headers={
                'X-Weather-Api-Cache-Hit': str(weather_result.data.get('cache_hit')),
                'Cache-Control': f'public, max-age={CACHE_TTL_MINS * 60}'
            }
        )
