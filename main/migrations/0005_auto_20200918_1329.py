# Generated by Django 2.2.4 on 2020-09-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_jobs_worked_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='electrical',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobs',
            name='garden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobs',
            name='pet_care',
            field=models.BooleanField(default=False),
        ),
    ]
