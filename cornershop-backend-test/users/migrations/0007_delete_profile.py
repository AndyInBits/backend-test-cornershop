# Generated by Django 3.0.8 on 2021-06-22 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_profile_picture'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
