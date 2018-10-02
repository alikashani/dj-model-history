#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core import management

from tests.models import Animal


class TrackedLifecycleModelTest(TestCase):

    def setUp(self):
        # TODO: load fixtures just once
        management.call_command('loaddata', 'animal.json', verbosity=0)
        management.call_command('loaddata', 'modelaction.json', verbosity=0)

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)

    # *************************************************************************
    # ***************************** ModelLog tests ****************************
    # *************************************************************************

    def test_all_logs_actions_not_none(self):
        animals = Animal.objects.all()
        deleted, _row_count, logs_created = animals.delete()
        logs_with_actions = [
            log for log in logs_created if log.action is not None
        ]
        self.assertEqual(len(logs_created), len(logs_with_actions))

    def test_all_logs_app_labels_match_model_app_label(self):
        animals = Animal.objects.all()
        deleted, _row_count, logs_created = animals.delete()
        self.assertEqual(logs_created[0].app_label, Animal._meta.app_label)

    def test_all_logs_created_with_same_app_label(self):
        animals = Animal.objects.all()
        deleted, _row_count, logs_created = animals.delete()
        app_label_set = {log.app_label for log in logs_created}
        self.assertEqual(len(app_label_set), 1)

    def test_all_logs_model_name_match_model_name(self):
        animals = Animal.objects.all()
        deleted, _row_count, logs_created = animals.delete()
        self.assertEqual(logs_created[0].model_name, Animal.__name__)

    def test_all_logs_created_with_same_model_name(self):
        animals = Animal.objects.all()
        deleted, _row_count, logs_created = animals.delete()
        model_name_set = {log.model_name for log in logs_created}
        self.assertEqual(len(model_name_set), 1)

    # *************************************************************************
    # ***************************** Deletion tests ****************************
    # *************************************************************************

    def test_log_created_for_each_deleted_model_instance(self):
        animals = Animal.objects.all()
        deleted, _row_count, logs_created = animals.delete()
        self.assertEqual(len(logs_created), _row_count.get('tests.Animal'))

    def test_deletion_logs_contain_delete_action_name(self):
        animals = Animal.objects.all()
        deleted, _row_count, logs_created = animals.delete()
        action_names = map(lambda log: log.action.name, logs_created)
        for name in action_names:
            self.assertEqual(name, 'Delete')

    def test_default_deletion_behavior_in_tact(self):
        animals = Animal.objects.all()
        count = animals.count()
        deleted, _row_count, logs_created = animals.delete()
        self.assertEqual(count, _row_count.get('tests.Animal'))

    # *************************************************************************
    # ***************************** Creation tests ****************************
    # *************************************************************************

    def test_log_created_for_created_model_instance(self):
        doggo, log = Animal.objects.create(
            name='Doggo',
            scientific_name='Woofus Doggolius',
            tooth_count=1,
            is_carnivore=False,
        )
        self.assertIsNotNone(log)

    def test_default_creation_behavior_in_tact(self):
        kwargs = dict(
            name='Doggo',
            scientific_name='Woofus Doggolius',
            tooth_count=1,
            is_carnivore=False,
        )
        doggo, log = Animal.objects.create(**kwargs)

        self.assertIsNotNone(doggo)

        self.assertIsInstance(doggo.tooth_count, int)
        self.assertEqual(doggo.tooth_count, kwargs.get('tooth_count'))

        self.assertIsInstance(doggo.is_carnivore, bool)
        self.assertEqual(doggo.is_carnivore, kwargs.get('is_carnivore'))

        self.assertIsInstance(doggo.name, str)
        self.assertEqual(doggo.name, kwargs.get('name'))

        self.assertIsInstance(doggo.scientific_name, str)
        self.assertEqual(doggo.scientific_name, kwargs.get('scientific_name'))

    def test_creation_log_contains_correct_data(self):
        kwargs = dict(
            name='Doggo',
            scientific_name='Woofus Doggolius',
            tooth_count=1,
            is_carnivore=False,
        )
        doggo, log = Animal.objects.create(**kwargs)

        self.assertIsInstance(log.data['tooth_count'], int)
        self.assertEqual(log.data['tooth_count'], kwargs.get('tooth_count'))

        self.assertIsInstance(log.data['is_carnivore'], bool)
        self.assertEqual(log.data['is_carnivore'], kwargs.get('is_carnivore'))

        self.assertIsInstance(log.data['name'], str)
        self.assertEqual(log.data['name'], kwargs.get('name'))

        self.assertIsInstance(log.data['scientific_name'], str)
        self.assertEqual(
            log.data['scientific_name'], kwargs.get('scientific_name')
        )

    # *************************************************************************
    # ****************************** Update tests *****************************
    # *************************************************************************

    def test_default_update_behavior_in_tact(self):
        new_tooth_count = 32
        animals = Animal.objects.all()
        count = animals.count()
        rows, logs = animals.update(tooth_count=new_tooth_count)
        tooth_counts = animals.values_list('tooth_count', flat=True).distinct()
        self.assertEqual(len(tooth_counts), 1)
        self.assertEqual(tooth_counts[0], new_tooth_count)
        self.assertEqual(rows, count)

    def test_update_creates_log_for_each_updated_object(self):
        animals = Animal.objects.all()
        rows, logs = animals.update(tooth_count=32)
        self.assertEqual(len(logs), rows)

    def test_update_logs_contain_update_action_name(self):
        animals = Animal.objects.all()
        rows, logs = animals.update(tooth_count=32)
        action_names = map(lambda log: log.action.name, logs)
        for name in action_names:
            self.assertEqual(name, 'Update')

    # *************************************************************************
    # *************************** Restoration tests ***************************
    # *************************************************************************

    def test_model_log_restore_creates_instance_of_correct_model(self):
        animals = Animal.objects.filter(tooth_count__lte=20)
        deleted, _row_count, logs = animals.delete()
        obj, log = logs[0].restore()
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, Animal)
