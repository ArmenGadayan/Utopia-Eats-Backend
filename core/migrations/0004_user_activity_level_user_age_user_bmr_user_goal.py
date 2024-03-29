# Generated by Django 4.1.6 on 2023-03-19 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_user_height_user_height_inches_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activity_level',
            field=models.IntegerField(choices=[(1.2, 'Low'), (1.55, 'Moderate'), (1.9, 'High')], default=1.55),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='bmr',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='goal',
            field=models.CharField(choices=[('Lose', 'Lose'), ('Maintain', 'Maintain'), ('Gain', 'Gain')], default='Maintain', max_length=10),
        ),
    ]
