# Generated by Django 4.2.11 on 2024-09-09 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_category_description_alter_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('content', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='core.competition')),
            ],
        ),
    ]
