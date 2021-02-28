import os
import time
from common.enums import APP
import requests

from apps.baseapp import App
from common.enums import APPSTATUS
from constants import EXCHANGES_DIR, STATIC_DIR
from vars import ROOT_DIR


class ExchangeUpdater(App):
    """
        Updates CSV file of exchanges.
    """

    APP_ID = APP.EXCHANGE_UPDATER.value
    EXCHANGES = ['NASDAQ', 'NYSE', 'AMEX', 'NYSEARCA']
    STATUS = {}

    def __init__(self):
        super().__init__()
        self.dir_path = os.path.join(ROOT_DIR, STATIC_DIR, EXCHANGES_DIR)
        os.makedirs(self.dir_path, exist_ok=True)
        if len(self.STATUS) == 0:
            for exchange in self.EXCHANGES:
                self.STATUS[exchange] = APPSTATUS.READY

    def run(self, exchange):
        super().start()
        if self.STATUS[exchange] == APPSTATUS.READY:
            for key, status in self.STATUS.items():
                if status != APPSTATUS.READY:
                    time.sleep(2)
                self.download_file(exchange)
        super().stop()

    def download_file(self, exchange):
        file_path = os.path.join(self.dir_path, exchange)
        url = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange={0}&render=download'
        url = url.format(exchange)
        headers = {'user-agent': 'app/0.0.1'}
        r = requests.get(url, headers=headers)
        with open('{0}.csv'.format(file_path), 'wb') as output:
            output.write(r.content)

    def get(self, command):
        if command == 'available-exchanges':
            return {'exchanges': self.EXCHANGES}

    def execute(self, command, **kwargs):
        if command == 'update-exchange':
            exchange = kwargs['exchange']
            # self.run(exchange)
            # message = str(exchange) + " exchange has finished updating"
            message = 'Updater has sunset'
            return {'<MESSAGE>': message}
        return {}
