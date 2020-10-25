import re


def parse_word(word):
    word = word.strip()
    word = re.sub('[^A-Za-z0-9]+', '', word)
    return word
