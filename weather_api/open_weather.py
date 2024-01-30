# Call the Open Weather api for a given city
# Use aiohttp to make the request asynchronously
# Return a standard Result object

import aiohttp
import asyncio
from .result import Result, ok, err
from .env import ENV


async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


async def get_open_weather(raw_city: str, lang: str) -> Result:
    '''
    Call the Open Weather api for a given city
    '''

    try:
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
            return err({
                'status': json.get('cod'),
                'message': json.get('message'),
            })

    except Exception as e:
        print('get_open_weather exception:', e)
        return err(e)
