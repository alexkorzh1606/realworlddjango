# Generated by Django 4.1 on 2022-09-14 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_enroll_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='enroll_count',
            field=models.CharField(max_length=6, verbose_name='Количество записей'),
        ),
    ]
