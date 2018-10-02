# -*- coding: utf-8 -*-

from django.db import models

from dj_model_history.models import TrackedLifecycleModel


class Animal(TrackedLifecycleModel):

    name = models.CharField(max_length=64)
    scientific_name = models.CharField(max_length=64)

    tooth_count = models.IntegerField(default=0)
    is_carnivore = models.BooleanField(default=False)

    def __str__(self):
        return self.name
