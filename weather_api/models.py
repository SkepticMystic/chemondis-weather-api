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
        # Convert wind_deg to to compass direction
        # Use 45deg offset to align with 4 cardinal directions
        wind_deg = data.get("wind").get("deg")
        if (wind_deg > 337.5):
            wind_direction = 'north'
        elif (wind_deg > 247.5):
            wind_direction = 'west'
        elif (wind_deg > 157.5):
            wind_direction = 'south'
        elif (wind_deg > 67.5):
            wind_direction = 'east'
        else:
            wind_direction = 'north'

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
            wind_direction=wind_direction,
            description=data.get("weather")[0].get("description"),
        )
