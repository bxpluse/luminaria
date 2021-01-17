import re


def parse_word(word):
    word = word.strip()
    word = re.sub('[^A-Za-z0-9]+', '', word)
    return word


def str_to_float(num: str):
    return float("{:.4f}".format(float(num)))


def flaot_to_float(num: float):
    return float("{:.4f}".format(num))
