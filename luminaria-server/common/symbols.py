import csv
import os

from constants import STATIC_DIR, BLACKLIST_FILENAME, WHITELIST_FILENAME, EXCHANGES_DIR
from vars import ROOT_DIR


def load_symbols():
    """
    :return: A set of all tickers in exchanges.
    """
    symbols = set()
    exchanges_path = os.path.join(ROOT_DIR, STATIC_DIR, EXCHANGES_DIR)
    for filename in os.listdir(exchanges_path):
        absolute_path = os.path.join(exchanges_path, filename)
        if os.path.isfile(absolute_path):
            ext = filename.split('.')[-1].lower()
            if ext == 'csv':
                s = load_csv(absolute_path)
            elif ext == 'txt':
                s = load_txt(absolute_path)
            else:
                s = set()
            symbols = symbols | s

    return purge_special_chars_from_set(symbols)


def load_csv(file_name):
    symbols = set()
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            symbols.add(row[0].strip())
    return symbols


def load_txt(file_name):
    symbols = set()
    with open(file_name) as file:
        for line in file:
            symbols.add(line.strip('\n'))
    return symbols


def load_blacklist():
    """
    :return: A set of symbols to not monitor for.
    """
    blacklist = set()
    filepath = os.path.join(ROOT_DIR, STATIC_DIR)
    for i in range(ord('A'), ord('Z') + 1):
        blacklist.add(chr(i))
    with open(os.path.join(filepath, BLACKLIST_FILENAME), 'a+') as file:
        file.seek(0)
        for word in file:
            blacklist.add(word.strip())
    return blacklist


def load_whitelist():
    """
    :return: A set of symbols to monitor for.
    """
    whitelist = set()
    filepath = os.path.join(ROOT_DIR, STATIC_DIR)
    with open(os.path.join(filepath, WHITELIST_FILENAME), 'a+') as file:
        file.seek(0)
        for word in file:
            whitelist.add(word.strip())
    return whitelist


def purge_special_chars_from_set(s):
    special_set = set()
    special_set.add('Symbol')
    special_set.add('')
    special_set.add(' ')
    special_set.add('  ')
    special_set.add('\n')
    return s - special_set
