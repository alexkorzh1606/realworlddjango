# Generated by Django 4.1 on 2022-09-14 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_places_left_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='places_left_count',
        ),
    ]
