# -*- coding: utf-8 -*-

import json
from importlib import import_module

from django.db import models

from dj_model_history.querysets import TrackedQuerySet


class TimeStampedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TrackedLifecycleModel(TimeStampedModel):

    objects = TrackedQuerySet.as_manager()

    class Meta:
        abstract = True


class ModelAction(models.Model):
    """
    Denotes the action performed on a model instance
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class ModelLog(models.Model):
    """
    Stores the action taken on a QuerySet (create, update, delete)
    and enables the restoration
    """

    _data = models.TextField()
    action = models.ForeignKey(ModelAction, null=True)

    app_label = models.CharField(max_length=64)
    model_name = models.CharField(max_length=64)

    def __str__(self):
        return '%s: %s' % (self.action.name, self.model_name)

    @property
    def data(self):
        return json.loads(self._data)

    def restore(self, model_dir=None):
        if model_dir is None:
            model_dir = 'models'

        models_ = import_module('%s.%s' % (self.app_label, model_dir))
        model = getattr(models_, self.model_name)
        obj = model.objects.create(**self.data)
        return obj
