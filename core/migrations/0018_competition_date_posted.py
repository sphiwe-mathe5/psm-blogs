# Generated by Django 4.2.11 on 2024-09-11 19:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_competition_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
