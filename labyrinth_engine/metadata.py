def add_meta(obj, *args, **kwargs):
    if 'metadata' not in obj.__dict__:
        obj.metadata = {}
    obj.metadate.update({key: True for key in args})
    obj.metadate.update(kwargs)
    return obj.metadate


def get_meta(obj):
    if 'metadata' not in obj.__dict__:
        return {}
    return obj.metadata
