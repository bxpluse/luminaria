import requests
from apscheduler.schedulers.background import BackgroundScheduler

from apps.baseapp import App
from common.enums import APP
from common.enums import APPTYPE
from config import SCHEDULER_TIME_ZONE
from database.ipo_strings_model import IPOStringModel
from database.local_config_model import LocalConfigModel


class IPOListener(App):

    APP_ID = APP.IPO_LISTENER.value

    def __init__(self):
        super().__init__(app_type=APPTYPE.STREAMING)
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': SCHEDULER_TIME_ZONE})
        self.scheduler.start()
        self.MAIN_SITE = LocalConfigModel.retrieve("IPO_CALENDAR_MARKETWATCH")
        self.SITES = [self.MAIN_SITE,
                      LocalConfigModel.retrieve("IPO_CALENDAR_YAHOO"),
                      LocalConfigModel.retrieve("IPO_CALENDAR_NASDAQ")]

    def run(self):
        super().start()
        self.scheduler.add_job(self.search, trigger='cron', second='*/6')
        # Search once on restarting application
        self.search()

    def search(self):
        try:
            terms = IPOStringModel.get_all_not_found_strings()
            response = requests.get(self.MAIN_SITE)
            cleaned = response.content.decode('utf-8').lower()
            for term in terms:
                res = cleaned.find(term.lower())
                if res >= 0:
                    IPOStringModel.update_string_as_found(term)
                    self.info("Company IPO announced: " + term)
        except Exception as e:
            self.info("ERROR: " + (repr(e)))
            self.info("Jobs after catching exception: " + str(self.scheduler.get_jobs()))

    @staticmethod
    def add_string(string):
        IPOStringModel.insert_string_if_not_exists(string)

    @staticmethod
    def remove_string(string):
        IPOStringModel.remove_string_if_not_found(string)

    @staticmethod
    def dismiss_string(string):
        IPOStringModel.update_string_as_dismissed(string)

    def get_data(self):
        res = IPOStringModel.get_all_not_dismissed_strings()
        return {'res': res, 'sites': self.SITES}

    def execute(self, command, **kwargs):
        string = kwargs['string']
        if command == 'add':
            self.add_string(string)
        elif command == 'remove':
            self.remove_string(string)
        elif command == 'dismiss':
            self.dismiss_string(string)
        return {}
