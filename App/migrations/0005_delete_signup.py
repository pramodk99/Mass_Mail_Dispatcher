# Generated by Django 3.2.14 on 2022-08-02 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_signup_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='signup',
        ),
    ]