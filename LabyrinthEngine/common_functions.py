def get_attr_safe(obj, attr, default_value):
    if hasattr(obj, attr):
        return obj.__dict__[attr]
    else:
        return default_value


def append_safe(obj, attr, key, value=None):
    if not hasattr(obj, attr):
        if value is None:
            obj.__dict__[attr] = [key]
        else:
            obj.__dict__[attr] = {key: value}
    else:
        if value is None:
            obj.__dict__[attr].append(key)
        else:
            obj.__dict__[attr][key] = value


def add_safe(obj, attr, value):
    if hasattr(obj, attr):
        obj.__dict__[attr].add(value)
    else:
        obj = set([value])


def remove_safe(obj, attr, value):
    if hasattr(obj, attr):
        obj.__dct__[attr].discard(value)