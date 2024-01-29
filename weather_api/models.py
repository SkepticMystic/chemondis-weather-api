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
        if (wind_deg <= 45):
            wind_direction = "N"
        elif (wind_deg <= 135):
            wind_direction = "E"
        elif (wind_deg <= 225):
            wind_direction = "S"
        elif (wind_deg <= 315):
            wind_direction = "W"
        else:
            wind_direction = "N"

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
