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
