def parse_word(word):
    # word = word.strip()
    # word = re.sub('[^A-Za-z0-9]+', '', word)
    # word = re.sub(r'^\W+', '', word)
    strp_chars = ' ~!@#$%^&*()_+-=[]{};:<>,./?|\n'
    word = word.strip(strp_chars)
    return word


def str_to_float(num: str):
    return float("{:.4f}".format(float(num)))


def flaot_to_float(num: float):
    return float("{:.4f}".format(num))


def type_transform(val, data_type):
    if data_type == 'int':
        val = int(val)
    elif data_type == 'float':
        val = float(val)
    elif data_type == 'bool':
        val = bool(val)
    elif data_type == 'list':
        val = eval(val)
    return val
