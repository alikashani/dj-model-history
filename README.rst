=============================
django_model_history
=============================

.. image:: https://badge.fury.io/py/dj-model-history.svg
    :target: https://badge.fury.io/py/dj-model-history

.. image:: https://travis-ci.org/alikashani/dj-model-history.svg?branch=master
    :target: https://travis-ci.org/alikashani/dj-model-history

.. image:: https://codecov.io/gh/alikashani/dj-model-history/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/alikashani/dj-model-history

Track the lifecycle of your django project's models

Documentation
-------------

The full documentation is at https://dj-model-history.readthedocs.io.

Quickstart
----------

Install django_model_history::

    pip install dj-model-history

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_model_history.apps.DjModelHistoryConfig',
        ...
    )

Create a model and subclass `TrackedLifecycleModel`

.. code-block:: python

    from dj_model_history import TrackedLifecycleModel


    class MyModel(TrackedLifecycleModel):
        name = models.CharField(max_length=128)



Features
--------

The following QuerySet methods of subclassed models will generate `ModelLog` objects
containing data about the action ("Create", "Update" or "Delete"), the model's app label,
name, & data:

- `create`
- `update`
- `delete`

.. code-block:: python

    from myapp.models import MyModel


    # Create
    obj, log = MyModel.objects.create(name='Object')

    # Update
    objs = MyModel.objects.all()
    rows, logs = objs.update(name='MyObject')

    # Delete
    deleted, row_count, logs = objs.delete()


Deleted objects can be restored

.. code-block:: python

    from dj_model_history import ModelLog

    deletion_log = ModelLog.objects.filter(action__name='Delete').first()
    obj, log = deletion_log.restore()
    obj  # MyModel instance

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage9)l
