from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=180)
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
        return f'{self.city} ({self.lang}) - {self.timestamp}'
