from datetime import datetime, timedelta
import pytz
import asyncio
from .open_weather import get_open_weather
from .result import Result, ok, err
from .models import Weather
from django.db.models import Q
from .env import ENV


CACHE_TTL_MINS = ENV.get('CACHE_TTL_MINS')


def refresh_cache(raw_city: str, lang: str) -> Result:
    '''
    Call the open weather api and save the result to the db
    '''

    # call open weather api
    open_weather_result = asyncio.run(get_open_weather(raw_city, lang))
    if (not open_weather_result.ok):
        return open_weather_result  # Returning early if there's an error

    # save to db
    try:
        weather = Weather.open_weather_to_model(
            raw_city,
            lang,
            open_weather_result.data
        )

        weather.save()

        return ok(weather)

    except Exception as e:
        print('refresh_cache exception:', e)
        return err({'status': 500, 'message': 'Error caching weather'})


class WeatherCache():

    def get_weather(raw_city: str, lang: str) -> Result:
        """
        Try get a cached value,
        Call Open Weather if needed
        """

        timestamp__gte = datetime.now(pytz.utc) -\
            timedelta(minutes=CACHE_TTL_MINS)

        # Implication is that the cache 'key' is city + lang
        # NOTE: We search the cache for raw_ or resolved_city,
        #       OpenWeather geocodes multiple inputs to the same output
        weather = Weather.objects.filter(
            (
                Q(raw_city=raw_city) |
                Q(resolved_city__iexact=raw_city)
            ) &
            Q(lang=lang) &
            Q(timestamp__gte=timestamp__gte)
        ).last()

        cache_hit = weather is not None
        if (not cache_hit):
            # Either we don't have a cached result, or it's too old
            refresh_result = refresh_cache(raw_city, lang)

            if (not refresh_result.ok):
                return refresh_result

            else:
                weather = refresh_result.data

        return ok({
            'cache_hit': cache_hit,
            'weather': weather
        })
