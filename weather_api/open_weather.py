import aiohttp
import asyncio
from .result import Result, ok, err
from .env import ENV


async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


# Example json response:
# {
#     'coord': {
#         'lon': -0.1257,
#         'lat': 51.5085
#     },
#     'weather': [{
#         'id': 804,
#         'main': 'Clouds',
#         'description': 'overcast clouds',
#         'icon': '04d'
#     }],
#     'base': 'stations',
#     'main': {
#         'temp': 281.58,
#         'feels_like': 279.43,
#         'temp_min': 280.75,
#         'temp_max': 282.21,
#         'pressure': 1031,
#         'humidity': 76
#     },
#     'visibility': 10000,
#     'wind': {
#         'speed': 3.6,
#         'deg': 200
#     },
#     'clouds': {
#         'all': 100
#     },
#     'dt': 1706368118,
#     'sys': {
#         'type': 2,
#         'id': 2075535,
#         'country': 'GB',
#         'sunrise': 1706341618,
#         'sunset': 1706373541
#     },
#     'timezone': 0,
#     'id': 2643743,
#     'name': 'London',
#     'cod': 200
# }

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


async def get_open_weather(raw_city: str, lang: str) -> Result:
    '''
    Call the Open Weather api for a given city
    '''

    try:
        # TODO: Sanitize & encode city input
        params = {
            'lang': lang,
            'q': raw_city,
            'units': 'metric',
            'appid': ENV.get('OPEN_WEATHER_API_KEY'),
        }

        url = f'{BASE_URL}?' + \
            '&'.join([f'{k}={v}' for k, v in params.items()])

        json = await get_json(url)

        if (json.get("cod") == 200):
            return ok(json)

        else:
            print('get_open_weather.cod != 200', json)
            return err({
                'status': json.get('cod'),
                'message': json.get('message'),
            })

    except Exception as e:
        print('get_open_weather exception:', e)
        return err(e)
