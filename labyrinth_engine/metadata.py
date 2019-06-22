def add_meta(obj, *args, **kwargs):
    if '_metadata' not in obj.__dict__:
        obj._metadata = {}
    obj._metadata.update({key: True for key in args})
    obj._metadata.update(kwargs)
    return obj._metadata


def get_meta(obj):
    if '_metadata' not in obj.__dict__:
        return {}
    return obj._metadata
