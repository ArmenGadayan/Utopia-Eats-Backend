# Generated by Django 4.1.6 on 2023-02-03 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_item_calories_alter_item_carbohydrates_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Item',
        ),
    ]
