# Generated by Django 4.1.4 on 2023-04-14 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('femlliga', '0005_alter_agreement_resource_alter_need_resource_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDenyList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]