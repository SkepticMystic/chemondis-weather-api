from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Allow any domain to access the API
        response['Access-Control-Allow-Origin'] = '*'
        # Allow specified HTTP methods
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        # Allow specified headers
        response['Access-Control-Allow-Headers'] = 'Content-Type, Accept'

        return response
