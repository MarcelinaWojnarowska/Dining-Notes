# Generated by Django 3.0.7 on 2020-11-17 16:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dining_notes', '0003_auto_20201113_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date_added',
            field=models.DateField(default=datetime.date(2020, 11, 17)),
        ),
        migrations.AlterField(
            model_name='note',
            name='meal',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack'), ('Supper', 'Supper')], max_length=10),
        ),
    ]
