# Generated by Django 5.0.3 on 2024-09-08 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0012_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_type',
        ),
    ]
