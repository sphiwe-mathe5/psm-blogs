# Generated by Django 5.0.3 on 2024-08-05 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0005_profile_is_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='service_pics')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_pictures', to='submit.profile')),
            ],
        ),
    ]
