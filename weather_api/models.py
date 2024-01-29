from django.db import models


class Weather(models.Model):
    raw_city = models.CharField(max_length=180)
    resolved_city = models.CharField(max_length=180)

    country = models.CharField(max_length=5)

    description = models.CharField(max_length=180)

    temp = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()

    pressure = models.FloatField()
    humidity = models.FloatField()

    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=5)

    lang = models.CharField(max_length=8)
    timestamp = models.DateTimeField(
        blank=True,
        auto_now=False,
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.resolved_city} ({self.lang}) - {self.timestamp}'

    def open_weather_to_model(raw_city, lang, data):
        return Weather(
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
