# Generated by Django 5.0.3 on 2024-08-10 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_post_category_post_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='location',
        ),
    ]
