import csv
import os

from constants import STATIC_DIR, BLACKLIST_FILENAME, WHITELIST_FILENAME, EXCHANGES_DIR
from vars import ROOT_DIR


def load_all_symbols():
    """
    :return: A set of all tickers in exchanges.
    """
    symbols = set()
    filepath = os.path.join(ROOT_DIR, STATIC_DIR)
    exchanges_path = os.path.join(ROOT_DIR, STATIC_DIR, EXCHANGES_DIR)
    for filename in os.listdir(exchanges_path):
        with open(os.path.join(exchanges_path, filename), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                symbols.add(row[0].strip())
    with open(os.path.join(filepath, WHITELIST_FILENAME), 'a+') as file:
        file.seek(0)
        for word in file:
            symbols.add(word.strip())
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
    with open(os.path.join(filepath, WHITELIST_FILENAME), 'a+') as file:
        file.seek(0)
        for word in file:
            if word in blacklist:
                blacklist.remove(word.strip())
    return blacklist
