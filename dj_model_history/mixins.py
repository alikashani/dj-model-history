import json
from importlib import import_module

from django.utils import six

models = import_module('dj_model_history.models')


# noinspection PyUnresolvedReferences, PyTypeChecker, PyProtectedMember
class ModelLogCreationMixin(object):
    """
    Handles creation of `ModelLog` objects documenting actions
    taken on model's instances
    # TODO: reduce `action_name` references
    """

    def create_model_logs(self, action_name):
        return models.ModelLog.objects.bulk_create(
            self.get_model_logs(action_name)
        )

    def get_model_logs(self, action_name):
        return map(lambda obj: self.instantiate_log(obj, action_name), self)

    def instantiate_log(self, instance, action_name=None):
        kwargs = {
            'app_label': self.model._meta.app_label,
            'model_name': instance.__class__.__name__,
            '_data': self.get_instance_data(instance)
        }
        if action_name is not None:
            kwargs.update(
                # TODO: avoid DB hit on each call
                {'action': models.ModelAction.objects.get(name=action_name)}
            )
        return models.ModelLog(**kwargs)

    def get_instance_data(self, obj):
        return json.dumps({
            key: self.process_value(value)
            for key, value in six.iteritems(obj.__dict__)
            if key != '_state'
        })

    @staticmethod
    def process_value(val):
        if isinstance(val, (bool, int)):
            return val
        return '%s' % val
