=====
Usage
=====

To use django_model_history in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_model_history.apps.DjModelHistoryConfig',
        ...
    )

Add django_model_history's URL patterns:

.. code-block:: python

    from dj_model_history import urls as dj_model_history_urls


    urlpatterns = [
        ...
        url(r'^', include(dj_model_history_urls)),
        ...
    ]
