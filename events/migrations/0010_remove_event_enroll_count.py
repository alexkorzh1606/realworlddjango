# Generated by Django 4.1 on 2022-09-14 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_event_enroll_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='enroll_count',
        ),
    ]
