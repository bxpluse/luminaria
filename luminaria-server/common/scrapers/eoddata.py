import os
import re
import string
import time
from urllib.request import build_opener, HTTPCookieProcessor

from bs4 import BeautifulSoup

from constants import STATIC_DIR, EXCHANGES_DIR
from vars import ROOT_DIR


def retrieve_by_letter(exchange, letter):
    site = 'http://eoddata.com/stocklist/{0}/{1}.htm'.format(exchange, letter)
    regex = '/stockquote/{}/(.*).htm'.format(exchange)
    s = set()
    res = []

    opener = build_opener(HTTPCookieProcessor())
    response = opener.open(site)
    html_page = response.read()
    soup = BeautifulSoup(html_page, "html.parser")

    # Search for every symbol found on site
    for link in soup.findAll('a'):
        href = link.get('href')
        search = re.search(regex, href)
        if search:
            symbol = search.group(1)
            if symbol not in s:
                s.add(symbol)
                res.append(symbol)
    return res


def download_from_exchange(exchange):
    exchanges_path = os.path.join(ROOT_DIR, STATIC_DIR, EXCHANGES_DIR)
    absolute_path = os.path.join(exchanges_path, exchange + '.txt')
    with open(absolute_path, 'w+') as file:
        for letter in string.ascii_uppercase[:27]:
            symbols = retrieve_by_letter(exchange, letter)
            for symbol in symbols:
                file.write(symbol + '\n')
            time.sleep(1.75)  # Prevent overloading site


if __name__ == '__main__':
    # download_from_exchange('TSX')
    # download_from_exchange('TSXV')
    pass
