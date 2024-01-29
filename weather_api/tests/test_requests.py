from django.test import TestCase


def get_weather(self: TestCase, city, lang=None):
    url = f'/weather/{city}'
    if lang:
        url += f'?lang={lang}'

    return self.client.get(url)


def safe_parse_json(response):
    try:
        return response.json()
    except Exception as e:
        return None


class TestRequests(TestCase):

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    # Check that a well-formed request is successful
    def test_happy_path(self):
        response = get_weather(self, 'london')
        self.assertEqual(response.status_code, 200)

        json = safe_parse_json(response)
        self.assertIsNotNone(json, response)
        self.assertTrue(json.get('ok'), json)

        data = json.get('data')
        self.assertIsNotNone(data, json)

        self.assertEquals(data.get('city'), 'London', json)

    # Check that a request with an invalid city name is rejected
    def test_city_not_found(self):
        response = get_weather(self, 'mumb')
        self.assertEqual(response.status_code, 404)

        json = safe_parse_json(response)
        self.assertIsNotNone(json, response)
        self.assertDictEqual(json, {
            'ok': False,
            'data': 'city not found',
        })

    # Check that subsequent requests for the same city are cached (within a short window)
    def test_second_request_is_cache_hit(self):
        city = 'mumbai'

        response_1 = get_weather(self, city)
        self.assertEqual(response_1.status_code, 200, response_1.status_code)

        json_1 = safe_parse_json(response_1)
        self.assertIsNotNone(json_1, response_1)
        self.assertTrue(json_1.get('ok'), json_1)

        response_2 = get_weather(self, city)
        self.assertEqual(response_2.status_code, 200, response_2.status_code)

        json_2 = safe_parse_json(response_2)
        self.assertIsNotNone(json_2, response_2)
        self.assertTrue(json_2.get('ok'), json_2)

        # NOTE: Responses are cached on two levels: in the browser and the db
        # The browser cache is not tested here, since self.client.get() doesn't use it
        # So we check the db cache by looking at the response header
        self.assertEqual(
            response_2.headers.get('X-Weather-Api-Cache-Hit'),
            'True',
        )

        # The responses, including their timestamps, should be identical
        self.assertDictEqual(json_1, json_2)
