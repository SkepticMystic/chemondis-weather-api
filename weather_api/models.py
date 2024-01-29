from django.db import models

# Convert wind_deg to a compass direction


class CompassDirection(models.TextChoices):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


def wind_deg_to_direction(wind_deg: int):
    if (wind_deg <= 45):
        return CompassDirection.NORTH
    elif (wind_deg <= 135):
        return CompassDirection.EAST
    elif (wind_deg <= 225):
        return CompassDirection.SOUTH
    elif (wind_deg <= 315):
        return CompassDirection.WEST
    else:
        return CompassDirection.NORTH


class Weather(models.Model):
    # The user-supplied city field
    raw_city = models.CharField(max_length=180)
    # The value Open Weather resolves raw_city to
    resolved_city = models.CharField(max_length=180)

    country = models.CharField(max_length=5)

    description = models.CharField(max_length=180)

    temp = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()

    pressure = models.FloatField()
    humidity = models.FloatField()

    wind_speed = models.FloatField()
    wind_direction = models.CharField(
        max_length=5,
        choices=CompassDirection.choices
    )

    lang = models.CharField(max_length=8)
    timestamp = models.DateTimeField(
        blank=True,
        auto_now=False,
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.resolved_city} ({self.lang}) - {self.timestamp}'

    def open_weather_to_model(raw_city, lang, data):
        wind_deg = data.get("wind").get("deg")
        wind_direction = wind_deg_to_direction(wind_deg)

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
