# Generated by Django 5.0.6 on 2024-07-22 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('femlliga', '0018_organization_welcome_email_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcludeCommentWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
            ],
        ),
    ]
