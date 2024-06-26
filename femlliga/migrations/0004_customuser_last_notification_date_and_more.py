# Generated by Django 4.0.3 on 2022-04-11 08:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("femlliga", "0003_organization_description_alter_needimage_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="last_notification_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customuser",
            name="notifications_frequency",
            field=models.CharField(
                choices=[
                    ("DAILY", "Diàriament"),
                    ("WEEKLY", "Setmanalment"),
                    ("NEVER", "Mai"),
                ],
                default="WEEKLY",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="socialmedia",
            name="media_type",
            field=models.CharField(
                choices=[
                    ("EMAIL", "Correu electrònic"),
                    ("WEBSITE", "Lloc web"),
                    ("FACEBOOK", "Facebook"),
                    ("INSTAGRAM", "Instagram"),
                    ("TWITTER", "Twitter"),
                    ("LINKEDIN", "Linkedin"),
                    ("WHATSAPP", "Whatsapp"),
                ],
                max_length=30,
            ),
        ),
    ]
