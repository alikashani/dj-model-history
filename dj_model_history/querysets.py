from django.db.models.query import QuerySet

from dj_model_history.mixins import ModelLogCreationMixin


class TrackedQuerySet(ModelLogCreationMixin, QuerySet):

    def delete(self):
        logs_created = self.create_model_logs('Delete')
        deleted, _rows_count = super(TrackedQuerySet, self).delete()
        return deleted, _rows_count, logs_created

    def create(self, **kwargs):
        obj = super(TrackedQuerySet, self).create(**kwargs)
        log = self.instantiate_log(obj, action_name='Create')
        log.save()
        return obj, log

    def update(self, **kwargs):
        rows = super(TrackedQuerySet, self).update(**kwargs)
        logs_created = self.create_model_logs('Update')
        return rows, logs_created
