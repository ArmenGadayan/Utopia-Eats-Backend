# Generated by Django 4.1.6 on 2023-03-20 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bmr',
        ),
    ]
