# Generated by Django 5.0.3 on 2024-08-10 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0010_profile_user_type_alter_profile_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='avatar.jpg', upload_to='profile_pics'),
        ),
    ]
