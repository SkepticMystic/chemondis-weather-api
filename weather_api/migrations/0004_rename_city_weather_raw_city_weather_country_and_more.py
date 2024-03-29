# Generated by Django 5.0.1 on 2024-01-29 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_api', '0003_weather_lang'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weather',
            old_name='city',
            new_name='raw_city',
        ),
        migrations.AddField(
            model_name='weather',
            name='country',
            field=models.CharField(default='ZZ', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='resolved_city',
            field=models.CharField(default='', max_length=180),
            preserve_default=False,
        ),
    ]
