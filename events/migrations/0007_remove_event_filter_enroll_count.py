# Generated by Django 4.1 on 2022-09-14 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_rename_show_enroll_count_event_filter_enroll_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='filter_enroll_count',
        ),
    ]