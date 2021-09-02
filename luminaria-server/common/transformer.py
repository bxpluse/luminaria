import json

from playhouse.shortcuts import model_to_dict

DEFAULT_KEYS = ['datetime_created']


def model_to_dict_wrapper(model, keys=()):
    d = model_to_dict(model)
    for key in keys:
        if key in d and d[key] is not None:
            d[key] = str(d[key])
    for key in DEFAULT_KEYS:
        if key in d and d[key] is not None:
            d[key] = str(d[key])
    return d


def model_to_dict_unstringify(model, keys=()):
    d = model_to_dict(model)

    for key, value in d.items():
        if key in set(keys) and d[key] is not None:
            d[key] = str(d[key])
        else:
            if value[0] == '{' and value[-1] == '}':
                d[key] = json.loads(d[key])
    return d
