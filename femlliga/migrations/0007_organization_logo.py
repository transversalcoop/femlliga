# Generated by Django 4.2.5 on 2023-09-20 09:09

from django.db import migrations, models

import femlliga.models


class Migration(migrations.Migration):
    dependencies = [
        ("femlliga", "0006_contactdenylist"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=femlliga.models.organization_logos_directory_path,
                validators=[femlliga.models.LimitFileSize(10)],
            ),
        ),
    ]