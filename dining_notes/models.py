from django.db import models
from django.contrib.auth.models import User

import datetime


class Note(models.Model):
    MEAL_TYPE = (
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("Snack", "Snack"),
        ("Supper", "Supper"),

    )

    date_added = models.DateField(default=datetime.date.today())
    meal = models.CharField(max_length=10, choices=MEAL_TYPE)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


