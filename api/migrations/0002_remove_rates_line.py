# Generated by Django 4.0.6 on 2022-07-26 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rates',
            name='line',
        ),
    ]
