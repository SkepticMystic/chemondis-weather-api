from dotenv import get_key

CACHE_TTL_MINS = get_key('.env', 'CACHE_TTL_MINS')
if (
    CACHE_TTL_MINS is None or
    CACHE_TTL_MINS not in ['5', '10', '60']
):
    CACHE_TTL_MINS = 5
else:
    CACHE_TTL_MINS = int(CACHE_TTL_MINS)


OPEN_WEATHER_API_KEY = get_key('.env', 'OPEN_WEATHER_API_KEY')
if (OPEN_WEATHER_API_KEY is None or OPEN_WEATHER_API_KEY == ''):
    raise Exception('OPEN_WEATHER_API_KEY not found in .env')

ENV = {
    'CACHE_TTL_MINS': CACHE_TTL_MINS,
    'OPEN_WEATHER_API_KEY': OPEN_WEATHER_API_KEY,
}
