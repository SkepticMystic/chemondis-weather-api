# Generated by Django 5.0.1 on 2024-01-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=180)),
                ('temp_min', models.FloatField()),
                ('temp_max', models.FloatField()),
                ('pressure', models.FloatField()),
                ('humidity', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('wind_direction', models.CharField(max_length=5)),
                ('description', models.CharField(max_length=180)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]