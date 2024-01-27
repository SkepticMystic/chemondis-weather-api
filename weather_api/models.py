from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=180)

    temp_min = models.FloatField()
    temp_max = models.FloatField()

    pressure = models.FloatField()
    humidity = models.FloatField()

    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=5)

    description = models.CharField(max_length=180)

    timestamp = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return f'{self.city} - {self.timestamp}'
