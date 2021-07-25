import csv
import os

import requests

from apps.baseapp import App
from common.enums import APP
from constants import CONFIG_MAP, EXCHANGES_DIR, STATIC_DIR, ROOT_DIR

USER_AGENT = CONFIG_MAP['USER_AGENT']


class ExchangeUpdater(App):
    """
        Updates CSV file of exchanges.
    """

    APP_ID = APP.EXCHANGE_UPDATER
    FILE_NAME = 'ALL.CSV'
    URL = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true'
    HEADERS = {'User-Agent': USER_AGENT,
               'Referer': 'https://www.nasdaq.com',
               'Origin': 'https://www.nasdaq.com/',
               'Host': 'api.nasdaq.com'
               }

    def __init__(self):
        super().__init__()
        self.dir_path = os.path.join(ROOT_DIR, STATIC_DIR, EXCHANGES_DIR)
        os.makedirs(self.dir_path, exist_ok=True)

    def download(self):
        res = requests.get(self.URL, headers=self.HEADERS, timeout=30)
        json = res.json()
        data = json['data']

        fields = ['symbol',
                  'name',
                  'lastsale',
                  'netchange',
                  'pctchange',
                  'marketCap',
                  'country',
                  'ipoyear',
                  'volume',
                  'sector',
                  'industry',
                  'url']
        rows = data['rows']
        with open(os.path.join(self.dir_path, self.FILE_NAME), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def execute(self, command, **kwargs):
        if command == 'update':
            message = 'Updated!'
            try:
                self.download()
            except Exception as e:
                self.log('Error in updating symbols: ' + str(e))
                message = 'Failed!'
            return {'<MESSAGE>': message}
