# Generated by Django 5.0.2 on 2024-02-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("femlliga", "0011_customuser_distance_limit_km_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="offer",
            name="place_accessible",
            field=models.BooleanField(default=False),
        ),
    ]
