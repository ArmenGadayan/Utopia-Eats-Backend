# Generated by Django 4.1.6 on 2023-03-19 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_activity_level_user_age_user_bmr_user_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activity_level',
            field=models.FloatField(choices=[(1.2, 'Low'), (1.55, 'Moderate'), (1.9, 'High')], default=1.55),
        ),
    ]
