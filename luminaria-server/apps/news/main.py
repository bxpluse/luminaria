import requests
from bs4 import BeautifulSoup

from apps.baseapp import App
from common.cache import Cache
from common.enums import APP
from database.config.local_config_model import LocalConfigModel


class News(App):
    APP_ID = APP.NEWS

    def __init__(self):
        cache = Cache(LocalConfigModel.retrieve('TOPTEN_CACHE_DURATION_SECS'))
        super().__init__(cache=cache)
        self.USER_AGENT = self.configuration['USER_AGENT']
        self.BBN_URL = self.configuration['BBN_URL']
        self.HEADERS = {'User-Agent': self.USER_AGENT,
                        'Referer': self.BBN_URL,
                        'Origin': self.BBN_URL,
                        'Host': self.BBN_URL.split('//')[-1]
                        }

    def bbn(self):
        res = []
        prefix = '/news'

        session = requests.Session()
        session.cookies.set('exp_pref', 'AMER')

        session.headers['User-Agent'] = self.HEADERS['User-Agent']
        session.headers['Referer'] = self.HEADERS['Referer']
        session.headers['Origin'] = self.HEADERS['Origin']
        session.headers['Host'] = self.HEADERS['Host']

        page = session.get(self.BBN_URL)
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
                    item = {'title': str(title).strip(), 'url': self.BBN_URL + url}
                    res.append(item)
        return res

    def execute(self, command, **kwargs):
        if command == 'fetch-news':
            return {'articles': self.bbn()}
