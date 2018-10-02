class EmptyItem(object):
    pass


def lazy_import(module_path, model_name):
    """
    FIXME:
    May be better to adjust this to use ``importlib.import_module()``
    instead of using built-in ``__import__``
    """
    try:
        module = __import__(module_path, globals(), locals(), fromlist=[''])
    except ImportError:
        module = EmptyItem()
    return map(lambda imp: getattr(module, imp), [model_name])
