import requests
from bs4 import BeautifulSoup

from apps.baseapp import App
from common.cache import Cache
from common.enums import APP
from constants import CONFIG_MAP

USER_AGENT = CONFIG_MAP['USER_AGENT']
BBN_URL = CONFIG_MAP['BBN_URL']

HEADERS = {'User-Agent': USER_AGENT,
           'Referer': BBN_URL,
           'Origin': BBN_URL,
           'Host': BBN_URL.split('//')[-1]
           }


class News(App):

    APP_ID = APP.NEWS

    def __init__(self):
        cache = Cache(CONFIG_MAP['TOPTEN_CACHE_DURATION_SECS'])
        super().__init__(cache=cache)

    def bbn(self):
        res = []
        prefix = '/news'

        session = requests.Session()
        session.cookies.set('exp_pref', 'AMER')

        session.headers['User-Agent'] = HEADERS['User-Agent']
        session.headers['Referer'] = HEADERS['Referer']
        session.headers['Origin'] = HEADERS['Origin']
        session.headers['Host'] = HEADERS['Host']

        page = session.get(BBN_URL)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, 'html.parser')

        for link in soup.findAll('a'):
            valid_link = True
            title = link.string
            url = str(link.get('href'))

            if title is not None:
                if len(url) < 5:
                    valid_link = False
                else:
                    for i in range(len(prefix)):
                        if url[i] != prefix[i]:
                            valid_link = False

                if valid_link:
                    item = {'title': str(title).strip(), 'url': BBN_URL + url}
                    res.append(item)
        return res

    def execute(self, command, **kwargs):
        if command == 'fetch-news':
            return {'articles': self.bbn()}
