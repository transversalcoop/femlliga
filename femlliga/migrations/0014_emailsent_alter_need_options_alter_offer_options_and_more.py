# Generated by Django 5.0.2 on 2024-05-13 11:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('femlliga', '0013_alter_agreement_options_alter_contact_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_on', models.DateTimeField(auto_now_add=True)),
                ('sent_to', models.TextField()),
                ('subject', models.TextField()),
                ('body', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='need',
            name='options',
            field=models.ManyToManyField(blank=True, to='femlliga.resourceoption'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='options',
            field=models.ManyToManyField(blank=True, to='femlliga.resourceoption'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sent_on', models.DateTimeField(auto_now_add=True, verbose_name='Enviat el')),
                ('message', models.TextField(verbose_name='Missatge')),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='femlliga.agreement')),
                ('sent_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages_sent', to='femlliga.organization', verbose_name='Enviat per')),
            ],
            options={
                'ordering': ['sent_on'],
            },
        ),
    ]
