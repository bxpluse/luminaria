from playhouse.shortcuts import model_to_dict


def model_to_dict_wrapper(model, keys=()):
    d = model_to_dict(model)
    for key in keys:
        if key in d and d[key] is not None:
            d[key] = str(d[key])
    return d
