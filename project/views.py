from django.http import HttpResponse


def home_view(request):
    return HttpResponse("Welcome to the Weather API! Please use the /weather/{city} endpoint to get the weather for a city.")
