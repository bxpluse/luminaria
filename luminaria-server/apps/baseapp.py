from common.enums import APP
from common.enums import APPTYPE
from common.enums import ENVIRONMENT, APPSTATUS
from common.logger import LogLevel, log as log_to_db
from constants import ENV


class App:
    """
        Base class for all Apps to inherit from.
    """

    APP_ID = APP.BASE

    def __init__(self, app_type=APPTYPE.EXECUTABLE, cache=None):
        self.app_type = app_type
        if self.app_type == APPTYPE.STREAMING:
            self.status = APPSTATUS.STOPPED
        elif self.app_type == APPTYPE.EXECUTABLE:
            self.status = APPSTATUS.READY
        self.signal = None
        self.debugging = False
        self.first_start = True
        self.cache = cache

    def start(self):
        """ Called when an App is run. """
        self.log("~ App Starting")
        self.status = APPSTATUS.STARTED

    def stop(self):
        """ Called when an App is finished running or stopped. """
        if self.app_type == APPTYPE.STREAMING:
            self.log("~ App Stopping")
            self.status = APPSTATUS.STOPPED
        elif self.app_type == APPTYPE.EXECUTABLE:
            self.log("~ App Finished")
            self.status = APPSTATUS.READY

    def try_cache(self, hash_id):
        if self.has_cache():
            res = self.cache.fetch(hash_id)
            return res
        return None

    def store_to_cache(self, command, data, response):
        if self.has_cache():
            self.cache.store(command, data, response)

    def has_cache(self):
        return self.cache is not None

    def get_status(self):
        return self.status.value

    def get_data(self):
        return {}

    def log(self, message, level=LogLevel.INFO):
        """ Prints or logs information depending on environment. """
        if ENV == ENVIRONMENT.PROD:
            log_to_db(self.APP_ID.value, message, level)
        elif ENV == ENVIRONMENT.DEV:
            print('[{0}][{1}]'.format(self.APP_ID.value, level), message)

    def blob(self, command, data):
        """
        Returns an absolute path to a file.
        """
        return ''

    def execute(self, command, **kwargs):
        """
        Interface to execute a command.
        """
        return {}
